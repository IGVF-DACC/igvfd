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
    '''
    Audit ConstructLibrary objects for correct associated diseases specification.

    This function checks if ConstructLibrary objects with origins of disease-associated variants
    specify which associated_disease is relevant, and vice versa. If inconsistency is found,
    it raises an audit failure.

    Args:
        value (dict): The ConstructLibrary object to be audited.
        system (any): System specific parameters.

    Yields:
        AuditFailure: An AuditFailure object specifying the ConstructLibrary object that fails the check.
    '''
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
        yield AuditFailure('inconsistent variants and ontology metadata',
                           detail, level='NOT_COMPLIANT')


@audit_checker('ConstructLibrary', frame='object')
def audit_construct_library_plasmid_map(value, system):
    '''
    Audit ConstructLibrary objects for plasmid map document attachment.

    This function verifies that ConstructLibrary objects have a document of type "plasmid map"
    attached to them. If such a document is missing, the function raises an audit failure.

    Args:
        value (dict): The ConstructLibrary object to be audited.
        system (any): System specific parameters.

    Yields:
        AuditFailure: An AuditFailure object specifying the ConstructLibrary object that fails the check.
    '''
    map_counter = 0
    detail = (
        f'ConstructLibrary {audit_link(path_to_text(value["@id"]),value["@id"])} '
        f'does not have a plasmid map document attached.'
    )
    documents = value.get('documents', [])
    if documents == []:
        yield AuditFailure('missing plasmid map', detail, level='WARNING')
    else:
        for document in documents:
            document_obj = system.get('request').embed(document, '@@object?skip_calculated=true')
            if document_obj['document_type'] == 'plasmid map':
                map_counter += 1
                break
            else:
                continue
        if map_counter == 0:
            yield AuditFailure('missing plasmid map', detail, level='WARNING')
