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
    if 'donors' in value:
        donor_ids = value.get('donors')
        taxa_dict = {}
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            if donor_object.get('taxa'):
                taxa = donor_object.get('taxa')
                if taxa not in taxa_dict:
                    taxa_dict[taxa] = []
                taxa_dict[taxa].append(d)

        if 'Homo sapiens' in taxa_dict:
            detail = (
                f'Whole organism {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'specifies that it is of taxa Homo sapiens, this is disallowed.'
            )
            yield AuditFailure('incorrect taxa', detail, level='ERROR')
