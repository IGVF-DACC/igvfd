def function_with_docstring():
    '''
    [
        {
            "audit_description": "audit description",
            "audit_category": "audit category",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "audit description 2",
            "audit_category": "audit category 2",
            "audit_level": "WARNING"
        }
    ]
    '''
    pass


def function_with_docstring_improper_keys():
    '''
    [
        {
            "audit_detail": "audit description",
            "audit_category": "audit category",
            "audit_levels": "WARNING"
        }
    ]
    '''
    pass


def function_with_docstring_out_of_order():
    '''
    [
        {
            "audit_level": "WARNING",
            "audit_category": "audit category",
            "audit_description": "audit description"
        }
    ]
    '''
    pass


def function_without_docstring():
    pass


def function_with_non_json_docstring():
    '''This is a bad non-JSON docstring.'''
    pass
