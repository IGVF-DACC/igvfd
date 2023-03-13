from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('ConstructLibrary', frame='object')
def audit_construct_library_associated_diseases(value, system):
    '''ConstructLibrary objects with origins of disease-associated variants
    need to specify which associated_disease is relevant, and vice versa'''
    detail = ''
    origin_list = value.get('origins', [])
    if 'disease-associated variants' in origin_list:
        assoc_disease = value.get('associated_diseases', [])
        if assoc_disease != []:
            return
        else:
            detail = (
                f'ConstructLibrary {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has disease-associated variants listed in its origins, '
                f'but no ontology specified in associated_diseases.'
            )
    else:
        assoc_disease = value.get('associated_diseases', [])
        if assoc_disease != []:
            detail = (
                f'ConstructLibrary {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has the associated_diseases property but does not list '
                f'disease-associated variants in its origins property.'
            )
    if detail != '':
        yield AuditFailure('missing metadata',
                           detail, level='NOT_COMPLIANT')
