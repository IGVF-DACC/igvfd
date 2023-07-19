def function_with_docstring():
    '''
        audit_detail: This detail: has colons: and :
        multiple
        lines
        audit_category: audit category
        audit_levels: ERROR, WARNING
    '''
    pass


def function_with_docstring_improper_keys():
    '''
        audit_details: audit details
        audit_categories: audit categories
        audit_level: ERROR
    '''
    pass


def function_without_docstring():
    pass
