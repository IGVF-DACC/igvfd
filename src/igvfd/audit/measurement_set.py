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
    [
        {
            "audit_description": "Measurement sets with a multiome size are expected to have the corresponding amount of measurement sets (excluding itself) listed in related multiome datasets. Each of these datasets are expected to have the same multiome size and samples.",
            "audit_category": "inconsistent multiome datasets",
            "audit_level": "ERROR"
        }
    ]
    '''
    detail = ''
    related_multiome_datasets = value.get('related_multiome_datasets', [])
    multiome_size = value.get('multiome_size')
    if related_multiome_datasets == [] and multiome_size:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has a multiome size of {multiome_size}, but no related '
            f'multiome datasets.'
        )
        yield AuditFailure('inconsistent multiome datasets', detail, level='ERROR')
    elif related_multiome_datasets and multiome_size:
        if len(related_multiome_datasets) != multiome_size - 1:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a multiome size of {multiome_size}, but {len(related_multiome_datasets)} '
                f'related multiome datasets when {multiome_size - 1} are expected.'
            )
            yield AuditFailure('inconsistent multiome datasets', detail, level='ERROR')
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
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has associated sample(s): {samples_to_link} which are not the same associated sample(s) '
                f'of related multiome dataset(s): {datasets_with_different_samples}'
            )
            yield AuditFailure('inconsistent multiome datasets', detail, level='ERROR')
        if datasets_with_different_multiome_sizes:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a specified multiome size of {multiome_size}, which does not match the '
                f'multiome size of related multiome dataset(s): {datasets_with_different_multiome_sizes}'
            )
            yield AuditFailure('inconsistent multiome datasets', detail, level='ERROR')


@audit_checker('MeasurementSet', frame='object')
def audit_unspecified_protocol(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets are expected to specify the experimental protocol utilized for conducting the assay on protocols.io.",
            "audit_category": "missing protocol",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    if 'protocols' not in value:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has no protocol. '
        )
        yield AuditFailure('missing protocol', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_readout(value, system):
    '''
    [
        {
            "audit_description": "CRISPR-based and MPRA measurement sets are expected to specify a readout, other assays are not expected to include a readout specification.",
            "audit_category": "inconsistent readout",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "If a readout is specified it is expected to be different than the assay term.",
            "audit_category": "inconsistent readout",
            "audit_level": "ERROR"
        }
    ]
    '''
    assay_term = value.get('assay_term')
    assay = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay = assay.get('term_name')
    assays_with_readout = ['CRISPR screen',
                           'massively parallel reporter assay',
                           'cas mediated mutagenesis']
    if 'readout' in value:
        if assay not in assays_with_readout:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'a {assay} assay, but specifies a readout.'
            )
            yield AuditFailure('inconsistent readout', detail, level='ERROR')
        if assay_term == value.get('readout'):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} specifies '
                f'the same readout and assay term.'
            )
            yield AuditFailure('inconsistent readout', detail, level='ERROR')
    else:
        if assay in assays_with_readout:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'a {assay} assay and does not specify a readout.'
            )
            yield AuditFailure('inconsistent readout', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_modifications(value, system):
    '''
    [
        {
            "audit_description": "Modifications should be consistent for samples within a measurement set.",
            "audit_category": "inconsistent modifications",
            "audit_level": "ERROR"
        }
    ]
    '''
    samples = value.get('samples', [])
    modifications = []
    for sample in samples:
        sample_object = system.get('request').embed(sample, '@@object?skip_calculated=true')
        modifications.append(sorted(sample_object.get('modifications', [])))
    modifications = set(tuple(i) for i in modifications)
    if len(modifications) > 1:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
            f'samples with inconsistent modifications applied.'
        )
        yield AuditFailure('inconsistent modifications', detail, level='ERROR')


@audit_checker('MeasurementSet', frame='object')
def audit_CRISPR_screen_lacking_modifications(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets from CRISPR-based assays are expected to have a modification specified on their samples.",
            "audit_category": "missing modification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
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
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} is '
                f'a CRISPR screen assay but has no specified modification on its sample(s); '
                f'modifications are missing on {sample_detail}.'
            )
            yield AuditFailure('missing modification', detail, level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_preferred_assay_title(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets with a preferred assay title are expected to specify an appropriate assay term.",
            "audit_category": "inconsistent assays",
            "audit_level": "WARNING"
        }
    ]
    '''
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name')
    preferred_assay_title = value.get('preferred_assay_title', '')
    if preferred_assay_title and preferred_assay_title not in assay_object.get('preferred_assay_titles', []):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
            f'assay_term {assay_term_name}, but preferred_assay_title "{preferred_assay_title}".'
        )
        yield AuditFailure('inconsistent assays', detail, level='WARNING')


@audit_checker('MeasurementSet', frame='object')
def audit_missing_institutional_certification(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets for mapping assays involving samples with a human origin are expected to link to the relevant institutional certificates issued to a matching lab and award.",
            "audit_category": "missing nih certification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
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
            yield AuditFailure('missing nih certification', detail, level='NOT_COMPLIANT')
