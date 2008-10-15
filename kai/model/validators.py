"""Custom validators"""
import formencode

from kai.model import Human

class UniqueDisplayname(formencode.FancyValidator):
    def _to_python(self, value, state):
        if Human.get_displayname(value):
            raise formencode.Invalid('Display name already exists',
                                     value, state)
        else:
            return value


class UniqueEmail(formencode.FancyValidator):
    def _to_python(self, value, state):
        if Human.get_email(value):
            raise formencode.Invalid('Email address already exists', value,
                                     state)
        else:
            return value


class ValidLogin(formencode.FancyValidator):
    field_names = None
    validate_partial_form = False
    email = None
    answer = None
    password = None

    messages = {
        'badlogin': "Invalid email and/or password",
    }
    
    def validate_python(self, field_dict, state):
        errors = {}
        email = field_dict[self.email]
        password = field_dict[self.password]
        
        user = Human.get_email(email)
        
        if not user:
            errors[self.email] = self.message('badlogin', state)
        if not errors:
            valid_password = user.verify_password(password)
            if valid_password:
                field_dict['user'] = user
            else:
                errors[self.email] = self.message('badlogin', state)
        if errors:
            error_list = errors.items()
            error_list.sort()
            error_message = '<br>\n'.join(
                ['%s: %s' % (name, value) for name, value in error_list])
            raise formencode.Invalid(error_message,
                                     field_dict, state,
                                     error_dict=errors)
