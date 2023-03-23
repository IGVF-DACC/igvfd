from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


@audit_checker('MeasurementSet', frame='object')
def audit_related_multiome_datasets(value, system):
    '''MeasurementSet objects with a specified `multiome_size` should have
    links to other MeasurementSet objects specified in `related_multiome_datasets`
    with the same `multiome_size` and `samples`.'''
    detail = ''
    related_multiome_datasets = value.get('related_multiome_datasets', [])
    multiome_size = value.get('multiome_size')
    if related_multiome_datasets == [] and multiome_size:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has a mutliome size of {multiome_size}, but no related '
            f'multiome MeasurementSet object(s).'
        )
        yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
    elif related_multiome_datasets and multiome_size:
        samples = value.get('samples')
        for dataset in related_multiome_datasets:
            dataset_object = system.get('request').embed(dataset, '@@object?skip_calculated=true')
            different_samples = []
            different_multiome_sizes = []
            if set(samples) != set(dataset_object.get('samples')):
                different_samples.append(
                    f"{audit_link(path_to_text(dataset), dataset)} which has associated sample(s): {dataset_object.get('samples')}")
            if dataset_object.get('multiome_size') is None:
                different_multiome_sizes.append(
                    f'{audit_link(path_to_text(dataset), dataset)} which does not have a specified multiome size')
            elif multiome_size != dataset_object.get('multiome_size') and dataset_object.get('multiome_size') is not None:
                different_multiome_sizes.append(
                    f"{audit_link(path_to_text(dataset), dataset)} which has a multiome size of: {dataset_object.get('multiome_size')}")
        different_samples = ', '.join(different_samples)
        different_multiome_sizes = ', '.join(different_multiome_sizes)
        if different_samples:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has associated sample(s) {samples} does not have the same associated sample(s) '
                f'as related multiome MeasurementSet object(s): {different_samples}'
            )
            yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
        if different_multiome_sizes:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a specified multiome size of {multiome_size}, which does not match the '
                f'multiome size of related MeasurementSet object(s): {different_multiome_sizes}'
            )
            yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
