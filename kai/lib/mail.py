"""Tools for sending email."""
from email import Charset, Encoders
from email.MIMEText import MIMEText
from email.MIMEMultipart import MIMEMultipart
from email.MIMEBase import MIMEBase
from email.Header import Header
from email.Utils import formatdate, parseaddr, formataddr
import mimetypes
import os
import random
import smtplib
import socket
import time
import types

from paste.deploy.converters import asbool
from pylons import config

# Don't BASE64-encode UTF-8 messages so that we avoid unwanted attention from
# some spam filters.
Charset.add_charset('utf-8', Charset.SHORTEST, Charset.QP, 'utf-8')

# Default MIME type to use on attachments (if it is not explicitly given
# and cannot be guessed).
DEFAULT_ATTACHMENT_MIME_TYPE = 'application/octet-stream'

# Cache the hostname, but do it lazily: socket.getfqdn() can take a couple of
# seconds, which slows down the restart of the server.
class CachedDnsName(object):
    def __str__(self):
        return self.get_fqdn()

    def get_fqdn(self):
        if not hasattr(self, '_fqdn'):
            self._fqdn = socket.getfqdn()
        return self._fqdn

DNS_NAME = CachedDnsName()
DEFAULT_CHARSET = 'utf-8'

# Copied from Python standard library and modified to used the cached hostname
# for performance.
def make_msgid(idstring=None):
    """Returns a string suitable for RFC 2822 compliant Message-ID, e.g:

    <20020201195627.33539.96671@nightshade.la.mastaler.com>

    Optional idstring if given is a string used to strengthen the
    uniqueness of the message id.
    """
    timeval = time.time()
    utcdate = time.strftime('%Y%m%d%H%M%S', time.gmtime(timeval))
    pid = os.getpid()
    randint = random.randrange(100000)
    if idstring is None:
        idstring = ''
    else:
        idstring = '.' + idstring
    idhost = DNS_NAME
    msgid = '<%s.%s.%s%s@%s>' % (utcdate, pid, randint, idstring, idhost)
    return msgid

def force_unicode(s, encoding='utf-8', strings_only=False, errors='strict'):
    """
    Similar to smart_unicode, except that lazy instances are resolved to
    strings, rather than kept as lazy objects.

    If strings_only is True, don't convert (some) non-string-like objects.
    """
    if strings_only and isinstance(s, (types.NoneType, int)):
        return s
    if not isinstance(s, basestring,):
        if hasattr(s, '__unicode__'):
            s = unicode(s)
        else:
            s = unicode(str(s), encoding, errors)
    elif not isinstance(s, unicode):
        s = unicode(s, encoding, errors)
    return s

class BadHeaderError(ValueError):
    pass

class SafeMIMEText(MIMEText):
    def __setitem__(self, name, val):
        "Forbids multi-line headers, to prevent header injection."
        if '\n' in val or '\r' in val:
            raise BadHeaderError, "Header values can't contain newlines (got %r for header %r)" % (val, name)
        try:
            val = str(force_unicode(val))
        except UnicodeEncodeError:
            if name.lower() in ('to', 'from', 'cc'):
                result = []
                for item in val.split(', '):
                    nm, addr = parseaddr(item)
                    nm = str(Header(nm, DEFAULT_CHARSET))
                    result.append(formataddr((nm, str(addr))))
                val = ', '.join(result)
            else:
                val = Header(force_unicode(val), DEFAULT_CHARSET)
        MIMEText.__setitem__(self, name, val)

class SafeMIMEMultipart(MIMEMultipart):
    def __setitem__(self, name, val):
        "Forbids multi-line headers, to prevent header injection."
        if '\n' in val or '\r' in val:
            raise BadHeaderError, "Header values can't contain newlines (got %r for header %r)" % (val, name)
        try:
            val = str(force_unicode(val))
        except UnicodeEncodeError:
            if name.lower() in ('to', 'from', 'cc'):
                result = []
                for item in val.split(', '):
                    nm, addr = parseaddr(item)
                    nm = str(Header(nm, DEFAULT_CHARSET))
                    result.append(formataddr((nm, str(addr))))
                val = ', '.join(result)
            else:
                val = Header(force_unicode(val), DEFAULT_CHARSET)
        MIMEMultipart.__setitem__(self, name, val)

class SMTPConnection(object):
    """
    A wrapper that manages the SMTP network connection.
    """
    def __init__(self, host=None, port=None, username=None, password=None,
                 use_tls=None, fail_silently=False):
        self.host = host or config['smtp_server']
        self.port = port or config.get('smtp_port', 25)
        self.username = username or config.get('smtp_username', '')
        self.password = password or config.get('smtp_password', '')
        self.use_tls = (use_tls is not None) and use_tls or \
            asbool(config.get('smtp_use_tls', False))
        self.fail_silently = fail_silently
        self.connection = None

    def open(self):
        """
        Ensure we have a connection to the email server. Returns whether or not
        a new connection was required.
        """
        if self.connection:
            # Nothing to do if the connection is already open.
            return False
        try:
            self.connection = smtplib.SMTP(self.host, self.port)
            if self.use_tls:
                self.connection.ehlo()
                self.connection.starttls()
                self.connection.ehlo()
            if self.username and self.password:
                self.connection.login(self.username, self.password)
            return True
        except:
            if not self.fail_silently:
                raise

    def close(self):
        """Close the connection to the email server."""
        try:
            try:
                self.connection.quit()
            except socket.sslerror:
                # This happens when calling quit() on a TLS connection
                # sometimes.
                self.connection.close()
            except:
                if self.fail_silently:
                    return
                raise
        finally:
            self.connection = None

    def send_messages(self, email_messages):
        """
        Send one or more EmailMessage objects and return the number of email
        messages sent.
        """
        if not email_messages:
            return
        new_conn_created = self.open()
        if not self.connection:
            # We failed silently on open(). Trying to send would be pointless.
            return
        num_sent = 0
        for message in email_messages:
            sent = self._send(message)
            if sent:
                num_sent += 1
        if new_conn_created:
            self.close()
        return num_sent

    def _send(self, email_message):
        """A helper method that does the actual sending."""
        if not email_message.to:
            return False
        try:
            self.connection.sendmail(email_message.from_email,
                    email_message.recipients(),
                    email_message.message().as_string())
        except:
            if not self.fail_silently:
                raise
            return False
        return True

class EmailMessage(object):
    """
    A container for email information.
    """
    content_subtype = 'plain'
    multipart_subtype = 'mixed'
    encoding = None     # None => use settings default

    def __init__(self, subject='', body='', from_email=None, to=None, bcc=None,
            connection=None, attachments=None, headers=None):
        """
        Initialise a single email message (which can be sent to multiple
        recipients).

        All strings used to create the message can be unicode strings (or UTF-8
        bytestrings). The SafeMIMEText class will handle any necessary encoding
        conversions.
        """
        self.to = to or []
        self.bcc = bcc or []
        self.from_email = from_email or config.get('smtp_from', '')
        self.subject = subject
        self.body = body
        self.attachments = attachments or []
        self.extra_headers = headers or {}
        self.connection = connection

    def get_connection(self, fail_silently=False):
        if not self.connection:
            self.connection = SMTPConnection(fail_silently=fail_silently)
        return self.connection

    def message(self):
        encoding = self.encoding or DEFAULT_CHARSET
        msg = SafeMIMEText(force_unicode(self.body, DEFAULT_CHARSET), self.content_subtype, encoding)
        if self.attachments:
            body_msg = msg
            msg = SafeMIMEMultipart(_subtype=self.multipart_subtype)
            if self.body:
                msg.attach(body_msg)
            for attachment in self.attachments:
                if isinstance(attachment, MIMEBase):
                    msg.attach(attachment)
                else:
                    msg.attach(self._create_attachment(*attachment))
        msg['Subject'] = self.subject
        msg['From'] = self.from_email
        msg['To'] = ', '.join(self.to)
        msg['Date'] = formatdate()
        msg['Message-ID'] = make_msgid()
        if self.bcc:
            msg['Bcc'] = ', '.join(self.bcc)
        for name, value in self.extra_headers.items():
            msg[name] = value
        return msg

    def recipients(self):
        """
        Returns a list of all recipients of the email (includes direct
        addressees as well as Bcc entries).
        """
        return self.to + self.bcc

    def send(self, fail_silently=False):
        """Send the email message."""
        return self.get_connection(fail_silently).send_messages([self])

    def attach(self, filename=None, content=None, mimetype=None):
        """
        Attaches a file with the given filename and content. The filename can
        be omitted (useful for multipart/alternative messages) and the mimetype
        is guessed, if not provided.

        If the first parameter is a MIMEBase subclass it is inserted directly
        into the resulting message attachments.
        """
        if isinstance(filename, MIMEBase):
            assert content == mimetype == None
            self.attachments.append(filename)
        else:
            assert content is not None
            self.attachments.append((filename, content, mimetype))

    def attach_file(self, path, mimetype=None):
        """Attaches a file from the filesystem."""
        filename = os.path.basename(path)
        content = open(path, 'rb').read()
        self.attach(filename, content, mimetype)

    def _create_attachment(self, filename, content, mimetype=None):
        """
        Convert the filename, content, mimetype triple into a MIME attachment
        object.
        """
        if mimetype is None:
            mimetype, _ = mimetypes.guess_type(filename)
            if mimetype is None:
                mimetype = DEFAULT_ATTACHMENT_MIME_TYPE
        basetype, subtype = mimetype.split('/', 1)
        if basetype == 'text':
            attachment = SafeMIMEText(content, subtype, DEFAULT_CHARSET)
        else:
            # Encode non-text attachments with base64.
            attachment = MIMEBase(basetype, subtype)
            attachment.set_payload(content)
            Encoders.encode_base64(attachment)
        if filename:
            attachment.add_header('Content-Disposition', 'attachment', filename=filename)
        return attachment

class EmailMultiAlternatives(EmailMessage):
    """
    A version of EmailMessage that makes it easy to send multipart/alternative
    messages. For example, including text and HTML versions of the text is
    made easier.
    """
    multipart_subtype = 'alternative'

    def attach_alternative(self, content, mimetype=None):
        """Attach an alternative content representation."""
        self.attach(content=content, mimetype=mimetype)
