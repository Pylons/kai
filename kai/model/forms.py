from formencode import Schema, validators

class AddSnippet(Schema):
    allow_extra_fields  = False
    filter_extra_fields = True
    
    title               = validators.UnicodeString(not_empty=True)
    description         = validators.UnicodeString(not_empty=True)
    content             = validators.UnicodeString(not_empty=True)