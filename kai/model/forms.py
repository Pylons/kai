from formencode import All, Schema
from formencode.validators import FieldsMatch
from tw import forms
from tw.api import WidgetsList
from tw.forms.validators import UnicodeString, Email

from kai.model.validators import ExistingEmail, UniqueDisplayname, UniqueEmail, ValidLogin, ValidPassword

forms.FormField.engine_name = "mako"

class FilteringSchema(Schema):
    filter_extra_fields = False
    allow_extra_fields = True
    ignore_key_missing = False


class SecureToken(forms.HiddenField):
    template = 'kai.templates.widgets.secure'


class ChangePasswordForm(forms.TableForm):
    class fields(WidgetsList):
        password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        confirm_password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        _authentication_token = SecureToken()
changepass_validator = FilteringSchema(
    chained_validators=[FieldsMatch('password', 'confirm_password')])
change_password_form = ChangePasswordForm('change_password_form', validator=changepass_validator)


class ForgotPasswordForm(forms.TableForm):
    class fields(WidgetsList):
        email_address = forms.TextField(
            label = 'Email',
            validator = ExistingEmail(not_empty=True))
        _authentication_token = SecureToken()
forgot_password_form = ForgotPasswordForm('forgot_password_form')


class LoginForm(forms.TableForm):
    class fields(WidgetsList):
        email_address = forms.TextField(
            validator = Email(not_empty=True))
        password = forms.PasswordField(
            validator = UnicodeString(not_empty=True))
        _authentication_token = SecureToken()
login_validator = FilteringSchema(
    chained_validators=[ValidLogin(email='email_address', password='password')])
login_form = LoginForm('login_form', validator=login_validator)


class RegistrationForm(forms.TableForm):
    class fields(WidgetsList):
        displayname = forms.TextField(
            validator = All(UnicodeString(not_empty=True), UniqueDisplayname()))
        email_address = forms.TextField(
            validator = All(Email(not_empty=True), UniqueEmail()))
        password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
        confirm_password = forms.PasswordField(
            validator = ValidPassword(not_empty=True))
registration_validator = FilteringSchema(
    chained_validators=[FieldsMatch('password', 'confirm_password')])
registration_form = RegistrationForm('registration_form', validator=registration_validator)


class AddSnippet(FilteringSchema):
    title = UnicodeString(not_empty=True)
    description = UnicodeString(not_empty=True)
    content = UnicodeString(not_empty=True)
    tags = UnicodeString()
