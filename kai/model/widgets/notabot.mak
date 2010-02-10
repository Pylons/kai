<%namespace name="tw" module="tw2.core.mako_util"/>\
<%!
from webhelpers.html.tools import js_obfuscate
%>
${js_obfuscate('<input type="hidden" name="notabot" %s' % tw.attrs(attrs=w.attrs)) | n}