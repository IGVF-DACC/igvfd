from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('CuratedSet', frame='object')
def audit_curated_set_mismatched_taxa(value, system):
    '''
        audit_detail: The taxa of the curated set and associated samples or donors are expected to be matching.
        audit_category: inconsistent taxa metadata
        audit_levels: ERROR
    '''
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
                f'CuratedSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a taxa which does not match the taxa of the associated Samples.'
            )
            yield AuditFailure('inconsistent taxa metadata', detail, level='ERROR')
    if 'donors' in value:
        donors_taxa = set(
            [
                system.get('request').embed(x + '@@object?skip_calculated=true').get('taxa', None)
                for x in value.get('donors', [])
            ]
        )
        if donors_taxa != taxa and '' not in taxa:
            detail = (
                f'CuratedSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a taxa which does not match the taxa of the associated Donors.'
            )
            yield AuditFailure('inconsistent taxa metadata', detail, level='ERROR')
