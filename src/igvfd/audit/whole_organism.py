from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('WholeOrganism', frame='object')
def audit_whole_organism_human_taxa(value, system):
    '''Flag whole organisms associated with taxa Homo sapiens.'''
    if value.get('taxa', '') == 'Homo sapiens':
        detail = (
            f'Whole organism {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'specifies that it is of taxa Homo sapiens, this is disallowed.'
        )
        yield AuditFailure('incorrect taxa', detail, level='ERROR')
