from snovault.auditor import (
    AuditFailure
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)
from .audit_registry import register_audit, register_all_audits


@register_audit(['WholeOrganism'], frame='object')
def audit_whole_organism_human_taxa(value, system):
    '''
    [
        {
            "audit_description": "Whole organisms are expected to have a model organism donor.",
            "audit_category": "unexpected donor",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_whole_organism_human_taxa)
    if 'taxa' in value:
        if value['taxa'] == 'Homo sapiens':
            detail = (
                f'Whole organism {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'specifies that it is of `taxa` Homo sapiens.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
    elif 'donors' in value:
        donor_ids = value.get('donors')
        taxa_set = set()
        for d in donor_ids:
            donor_object = system.get('request').embed(d + '@@object?skip_calculated=true')
            taxa_set.add(donor_object.get('taxa', ''))
        if 'Homo sapiens' in taxa_set:
            detail = (
                f'Whole organism {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'specifies that it has `donors` of `taxa` Homo sapiens.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


register_all_audits()
