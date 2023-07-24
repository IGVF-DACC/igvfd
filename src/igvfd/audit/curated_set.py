from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('CuratedSet', frame='object')
def audit_curated_set_mismatched_donor(value, system):
    '''
        audit_detail: The donor specified for curated set and the donor of the associated samples should be matching.
        audit_category: inconsistent donor metadata
        audit_levels: ERROR
    '''
    samples_donors = set()
    donors_specified = set()
    if ('samples' in value) and ('donors' in value):
        donors_specified = set(value['donors'])
        sample_ids = value.get('samples')
        for s in sample_ids:
            samples_object = system.get('request').embed(s + '@@object?skip_calculated=true')
            if 'donors' in samples_object:
                for d in samples_object['donors']:
                    samples_donors.add(d)

        if samples_donors != donors_specified:
            detail = (
                f'CuratedSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a donor(s) which does not match the donor(s) of the associated Samples.'
            )
            yield AuditFailure('inconsistent donors metadata', detail, level='ERROR')


@audit_checker('CuratedSet', frame='object')
def audit_curated_set_mismatched_taxa(value, system):
    '''
        audit_detail: The taxa specified for a curated set, the taxa of the associated samples, and the taxa of the associated donors should be identical.
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

    if 'donors' in value and \
            'samples' in value and \
            donors_taxa != samples_taxa and not \
            (donors_taxa == {'Mus musculus', 'Homo sapiens'} and samples_taxa == {None}):
        detail = (
            f'CuratedSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has Samples with taxa that do not match the taxa of the Donors.'
        )
        yield AuditFailure('inconsistent taxa metadata', detail, level='ERROR')
