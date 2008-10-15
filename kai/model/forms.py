from formencode import All, Schema
from formencode.validators import Email, FieldsMatch, UnicodeString

from kai.model.validators import UniqueDisplayname, UniqueEmail, ValidLogin

class FilterSchema(Schema):
    allow_extra_fields  = False
    filter_extra_fields = True

    
class AddSnippet(FilterSchema):
    title = UnicodeString(not_empty=True)
    description = UnicodeString(not_empty=True)
    content = UnicodeString(not_empty=True)
    tags = UnicodeString()


class LoginForm(FilterSchema):
    email = UnicodeString(not_empty=True)
    password = UnicodeString(not_empty=True)
    
    chained_validators = [
        ValidLogin(email='email', password='password')
    ]

class Registration(FilterSchema):
    displayname = All(UnicodeString(not_empty=True), UniqueDisplayname())
    email = All(Email(not_empty=True), UniqueEmail())
    email2 = Email(not_empty=True)
    password = UnicodeString(not_empty=True, min=6)
    password2 = UnicodeString(not_empty=True, min=6)
    
    chained_validators = [
        FieldsMatch('email', 'email2'),
        FieldsMatch('password', 'password2')
    ]


class OpenIDRegistration(FilterSchema):
    displayname = UnicodeString(not_empty=True)
    email = Email(not_empty=True)
    email2 = Email(not_empty=True)
    
    chained_validators = [
        FieldsMatch('email', 'email2'),
    ]
