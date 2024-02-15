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
def audit_unspecified_protocol(value, system):
    '''
        audit_detail: Measurement sets are expected to specify the experimental protocol utilized for conducting the assay on protocols.io.
        audit_category: missing protocol
        audit_levels: NOT_COMPLIANT
    '''
    if 'protocols' not in value:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'is expected to specify the experimental protocol utilized for conducting '
            f'the assay on protocols.io.'
        )
        yield AuditFailure('missing protocol', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_readout(value, system):
    '''
        audit_detail: CRISPR-based and MPRA assays are required to specify a readout, other assays should not include one.
        audit_category: inconsistent readout
        audit_levels: NOT_COMPLIANT
    '''
    assay_term = value.get('assay_term')
    assay = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assays_with_readout = ['CRISPR screen',
                           'massively parallel reporter assay',
                           'cas mediated mutagenesis']
    if assay.get('term_name') in assays_with_readout:
        if 'readout' not in value:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'a screening assay (such as CRISPR screen or MPRA) and is expected to specify a data readout.'
            )
            yield AuditFailure('inconsistent readout', detail, level='NOT_COMPLIANT')
    else:
        if 'readout' in value:
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'not expected to specify a data readout.'
            )
            yield AuditFailure('inconsistent readout', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_modifications(value, system):
    '''
        audit_detail: Modifications should be consistent for samples within a measurement set.
        audit_category: inconsistent modifications
        audit_levels: NOT_COMPLIANT
    '''
    samples = value.get('samples', [])
    modifications = []
    for sample in samples:
        sample_object = system.get('request').embed(sample, '@@object?skip_calculated=true')
        modifications.append(sorted(sample_object.get('modifications', [])))
    modifications = set(tuple(i) for i in modifications)
    if len(modifications) > 1:
        detail = (
            f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} has '
            f'samples with inconsistent modifications applied.'
        )
        yield AuditFailure('inconsistent modifications', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_CRISPR_screen_lacking_modifications(value, system):
    '''
        audit_detail: CRISPR screen and cas mediated mutagenesis measurement sets are required to have a modification specified on their samples.
        audit_category: missing modification
        audit_levels: ERROR
    '''
    assay_term = value.get('assay_term')
    assay = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    crispr_assays = ['cas mediated mutagenesis',
                     'CRISPR screen'
                     ]
    if assay.get('term_name') in crispr_assays:
        samples = value.get('samples', [])
        bad_samples = []
        for sample in samples:
            sample_object = system.get('request').embed(sample, '@@object?skip_calculated=true')
            if 'modifications' not in sample_object:
                bad_samples.append(sample)
        if bad_samples != []:
            samples_to_link = [audit_link(path_to_text(bad_sample), bad_sample) for bad_sample in bad_samples]
            sample_detail = samples_to_link = ', '.join(samples_to_link)
            detail = (
                f'MeasurementSet {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'a CRISPR screen assay and is expected to specify a modification on its sample(s); '
                f'modifications are missing on {sample_detail}.'
            )
            yield AuditFailure('missing modification', detail, level='ERROR')


@audit_checker('MeasurementSet', frame='object')
def audit_preferred_assay_title(value, system):
    '''
        audit_detail: Measurement sets with a preferred assay title are expected to specify an appropriate assay term.
        audit_category: inconsistent assay metadata
        audit_levels: WARNING
    '''
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name')
    preferred_assay_title = value.get('preferred_assay_title', '')
    if preferred_assay_title and preferred_assay_title not in assay_object.get('preferred_assay_titles', []):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
            f'assay term "{assay_term_name}", but preferred assay title "{preferred_assay_title}", '
            f'which is not an expected preferred assay title for this assay term.'
        )
        yield AuditFailure('inconsistent assay metadata', detail, level='WARNING')


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_institutional_certification(value, system):
    '''
        audit_detail: Measurement sets for mapping assays are expected to link to samples covered by an institutional certificate issued to a matching lab and award.
        audit_category: inconsistent institutional certification
        audit_levels: ERROR
    '''
    # Only audit Measurement Sets with at least one human sample.
    donors = value.get('donors', [])
    taxa = set()
    for d in donors:
        donor_obj = system.get('request').embed(d, '@@object?skip_calculated=true')
        taxa.add(donor_obj.get('taxa', ''))
    if 'Homo sapiens' not in taxa:
        return

    # Characterization assays do not need to be audited.
    characterization_assays = [
        'OBI:0003133',  # cas mediated mutagenesis
        'NTR:0000520',  # CRISPR screen
        'OBI:0000916',  # flow cytometry assay
        'OBI:0000185',  # imaging assay
        'OBI:0002675',  # massively parallel reporter assay',
        'OBI:0000288',  # protein-protein interaction detection assay',
        'OBI:0002041'  # self-transcribing active regulatory region sequencing assay
    ]
    assay_term = value.get('assay_term', '')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_id = assay_object.get('term_id', '')
    if assay_term_id in characterization_assays:
        return

    lab = value.get('lab', '')
    award = value.get('award', '')
    samples = value.get('samples', [])

    for s in samples:
        sample_object = system.get('request').embed(s, '@@object')
        nic_labs = []
        nic_awards = []
        for nic in sample_object.get('institutional_certificates', []):
            nic_object = system.get('request').embed(nic, '@@object?skip_calculated=true')
            nic_labs.append(nic_object.get('lab', ''))
            nic_awards.append(nic_object.get('award', ''))
        if lab not in nic_labs or award not in nic_awards:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
                f'a sample {audit_link(path_to_text(s),s)} that lacks a NIH institutional '
                f'certificate issued to the lab that submitted this file set.'
            )
            yield AuditFailure('inconsistent institutional certificate', detail, level='ERROR')
