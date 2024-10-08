from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


@audit_checker('CuratedSet', frame='object')
def audit_curated_set_mismatched_taxa(value, system):
    '''
    [
        {
            "audit_description": "The taxa of the curated set and associated samples or donors are expected to be matching.",
            "audit_category": "inconsistent taxa",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_curated_set_mismatched_taxa)
    taxa = {value.get('taxa', '')}
    samples_taxa = set()
    donors_taxa = set()
    if 'samples' in value:
        samples_taxa = set(
            [
                system.get('request').embed(x).get('taxa', None)
                for x in value.get('samples', [])
            ]
        )
        if samples_taxa != taxa and '' not in taxa:
            detail = (
                f'Curated set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a `taxa` which does not match the `taxa` of its associated `samples`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
    if 'donors' in value:
        donors_taxa = set(
            [
                system.get('request').embed(x + '@@object?skip_calculated=true').get('taxa', None)
                for x in value.get('donors', [])
            ]
        )
        if donors_taxa != taxa and '' not in taxa:
            detail = (
                f'Curated set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a `taxa` which does not match the `taxa` of its associated `donors`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
