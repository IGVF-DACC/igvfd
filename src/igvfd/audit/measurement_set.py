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
    '''
        audit_detail: Measurement sets with a specified multiome_size are expected to have the corresponding amount of links to other measurement sets (excluding itself) in related_multiome_datasets which are expected to have the same multiome_size and samples.
        audit_category: inconsistent multiome metadata
        audit_levels: WARNING
    '''
    detail = ''
    related_multiome_datasets = value.get('related_multiome_datasets', [])
    multiome_size = value.get('multiome_size')
    if related_multiome_datasets == [] and multiome_size:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has a multiome size of {multiome_size}, but no related '
            f'multiome MeasurementSet object(s).'
        )
        yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
    elif related_multiome_datasets and multiome_size:
        if len(related_multiome_datasets) != multiome_size - 1:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a multiome size of {multiome_size}, but {len(related_multiome_datasets)} '
                f'related multiome MeasurementSet object(s) when {multiome_size - 1} are expected.'
            )
            yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
        samples = value.get('samples')
        samples_to_link = [audit_link(path_to_text(sample), sample) for sample in samples]
        datasets_with_different_samples = []
        datasets_with_different_multiome_sizes = []
        for dataset in related_multiome_datasets:
            dataset_object = system.get('request').embed(dataset, '@@object?skip_calculated=true')
            if set(samples) != set(dataset_object.get('samples')):
                related_samples_to_link = [audit_link(path_to_text(sample), sample)
                                           for sample in dataset_object.get('samples')]
                datasets_with_different_samples.append(
                    f"{audit_link(path_to_text(dataset), dataset)} which has associated sample(s): {', '.join(related_samples_to_link)}")
            if dataset_object.get('multiome_size') is None:
                datasets_with_different_multiome_sizes.append(
                    f'{audit_link(path_to_text(dataset), dataset)} which does not have a specified multiome size')
            if multiome_size != dataset_object.get('multiome_size') and dataset_object.get('multiome_size') is not None:
                datasets_with_different_multiome_sizes.append(
                    f"{audit_link(path_to_text(dataset), dataset)} which has a multiome size of: {dataset_object.get('multiome_size')}")
        datasets_with_different_samples = ', '.join(datasets_with_different_samples)
        datasets_with_different_multiome_sizes = ', '.join(datasets_with_different_multiome_sizes)
        samples_to_link = ', '.join(samples_to_link)
        if datasets_with_different_samples:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has associated sample(s): {samples_to_link} which are not the same associated sample(s) '
                f'of related multiome MeasurementSet object(s): {datasets_with_different_samples}'
            )
            yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')
        if datasets_with_different_multiome_sizes:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a specified multiome size of {multiome_size}, which does not match the '
                f'multiome size of related MeasurementSet object(s): {datasets_with_different_multiome_sizes}'
            )
            yield AuditFailure('inconsistent multiome metadata', detail, level='WARNING')


@audit_checker('MeasurementSet', frame='object')
def audit_seqspec(value, system):
    '''
        audit_detail: Measurement sets are expected to specify the associated seqspec YAML file located in the seqspec repository: https://github.com/IGVF/seqspec.
        audit_category: missing seqspec
        audit_levels: WARNING
    '''
    if 'seqspec' not in value:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'are expected to specify the associated seqspec YAML file link located in '
            f'the seqspec repository: https://github.com/IGVF/seqspec.'
        )
        yield AuditFailure('missing seqspec', detail, level='WARNING')


@audit_checker('MeasurementSet', frame='object')
def audit_unspecified_protocol(value, system):
    '''
        audit_detail: Measurement sets are expected to specify the experimental protocol utilized for conducting the assay on protocols.io.
        audit_category: missing protocol
        audit_levels: NOT_COMPLIANT
    '''
    if 'protocol' not in value:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'are expected to specify the experimental protocol utilized for conducting '
            f'the assay on protocols.io.'
        )
        yield AuditFailure('missing protocol', detail, level='NOT_COMPLIANT')
