from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


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


def audit_curated_set_non_virtual_sample(value, system):
    '''
    [
        {
            "audit_description": "Curated sets are expected to link to only virtual samples.",
            "audit_category": "inconsistent samples",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_curated_set_non_virtual_sample)
    non_virtual_samples = []
    samples = value.get('samples', [])
    if samples:
        for sample in samples:
            sample_object = system.get('request').embed(sample, '@@object?skip_calculated=true')
            if not (sample_object.get('virtual', False)):
                non_virtual_samples.append(sample)
    if non_virtual_samples:
        non_virtual_samples = ', '.join(audit_link(path_to_text(non_virtual_sample), non_virtual_sample)
                                        for non_virtual_sample in non_virtual_samples)
        detail = (
            f'Curated set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to non-virtual sample(s): {non_virtual_samples}.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_curated_set_object = {
    'audit_curated_set_mismatched_taxa': audit_curated_set_mismatched_taxa,
    'audit_curated_set_non_virtual_sample': audit_curated_set_non_virtual_sample
}


@audit_checker('CuratedSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_curated_set_object.values()))
def audit_curated_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_curated_set_object.keys():
        for failure in function_dispatcher_curated_set_object[function_name](value, system):
            yield failure
