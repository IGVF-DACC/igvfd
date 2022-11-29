from snovault import (
    AuditFailure,
    audit_checker,
)
from .formatter import (
    audit_link,
    path_to_text,
)


def audit_curated_set_docs(value, system):
    if 'documents' not in value:
        return
    for doc in value['documents']:
        if doc.get('document_type') == 'characterization':
            detail = (
                f'CuratedSet {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'inappropriately contains a characterization document.'
            )
            yield AuditFailure('inconsistent characterization document',
                               detail, level='WARNING')
            return
        else:
            continue


function_dispatcher = {
    'audit_docs': audit_curated_set_docs
}


@audit_checker('File',
               frame=['curated_set_type'
                      'documents',
                      'documents.document_type',
                      ]
               )
def audit_curated_set(value, system):
    for function_name in function_dispatcher.keys():
        for failure in function_dispatcher[function_name](value, system):
            yield failure
