from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
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
    description = get_audit_description(audit_related_multiome_datasets)
    detail = ''
    related_multiome_datasets = value.get('related_multiome_datasets', [])
    multiome_size = value.get('multiome_size')
    if related_multiome_datasets == [] and multiome_size:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has a `multiome_size` of {multiome_size}, but no `related_multiome_datasets`.'
        )
        yield AuditFailure('inconsistent multiome datasets', f'{detail} {description}', level='ERROR')
    elif related_multiome_datasets and multiome_size:
        if len(related_multiome_datasets) != multiome_size - 1:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has a `multiome_size` of {multiome_size}, but {len(related_multiome_datasets)} '
                f'`related_multiome_datasets` when {multiome_size - 1} are expected.'
            )
            yield AuditFailure('inconsistent multiome datasets', f'{detail} {description}', level='ERROR')
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
                    f'{audit_link(path_to_text(dataset), dataset)} which does not have a specified `multiome_size`')
            if multiome_size != dataset_object.get('multiome_size') and dataset_object.get('multiome_size') is not None:
                datasets_with_different_multiome_sizes.append(
                    f"{audit_link(path_to_text(dataset), dataset)} which has a `multiome_size` of: {dataset_object.get('multiome_size')}")
        datasets_with_different_samples = ', '.join(datasets_with_different_samples)
        datasets_with_different_multiome_sizes = ', '.join(datasets_with_different_multiome_sizes)
        samples_to_link = ', '.join(samples_to_link)
        if datasets_with_different_samples:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has associated `samples`: {samples_to_link} which are not the same associated `samples` '
                f'of `related_multiome_datasets`: {datasets_with_different_samples}'
            )
            yield AuditFailure('inconsistent multiome datasets', f'{detail} {description}', level='ERROR')
        if datasets_with_different_multiome_sizes:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a specified `multiome_size` of {multiome_size}, which does not match the '
                f'`multiome_size` of `related_multiome_datasets`: {datasets_with_different_multiome_sizes}'
            )
            yield AuditFailure('inconsistent multiome datasets', f'{detail} {description}', level='ERROR')


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
    description = get_audit_description(audit_unspecified_protocol)
    if 'protocols' not in value:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has no `protocols`.'
        )
        yield AuditFailure('missing protocol', f'{detail} {description}', level='NOT_COMPLIANT')


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
    description = get_audit_description(audit_CRISPR_screen_lacking_modifications)
    assay_term = value.get('assay_term')
    assay = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    crispr_assays = ['proliferation CRISPR screen',
                     'CRISPR perturbation screen followed by flow cytometry and FISH',
                     'CRISPR perturbation screen followed by single-cell RNA sequencing',
                     'cas mediated mutagenesis']
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
                f'a CRISPR screen assay but has no specified `modifications` on its `samples`: {sample_detail}.'
            )
            yield AuditFailure('missing modification', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_preferred_assay_title(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets are expected to specify a preferred assay title.",
            "audit_category": "missing preferred assay title",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Measurement sets are expected to specify an appropriate preferred assay title for its respective assay term.",
            "audit_category": "inconsistent preferred assay title",
            "audit_level": "WARNING"
        }
    ]
    '''
    description_missing = get_audit_description(audit_preferred_assay_title, index=0)
    description_inconsistent = get_audit_description(audit_preferred_assay_title, index=1)
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name')
    preferred_assay_title = value.get('preferred_assay_title', '')
    if preferred_assay_title:
        if preferred_assay_title not in assay_object.get('preferred_assay_titles', []):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
                f'`assay_term` {assay_term_name}, but `preferred_assay_title` {preferred_assay_title}.'
            )
            yield AuditFailure('inconsistent preferred assay title', f'{detail} {description_inconsistent}', level='WARNING')
    else:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} has '
            f'no `preferred_assay_title`.'
        )
        yield AuditFailure('missing preferred assay title', f'{detail} {description_missing}', level='NOT_COMPLIANT')


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
    description = get_audit_description(audit_missing_institutional_certification)
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
                f'a sample {audit_link(path_to_text(s),s)} that lacks any `institutional_certificates` '
                f'issued to the lab that submitted this file set.'
            )
            yield AuditFailure('missing nih certification', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='embedded')
def audit_CRISPR_screen_missing_gRNA_sequencing_auxiliary_set(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets from CRISPR-based assays are expected to link to a gRNA sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_CRISPR_screen_missing_gRNA_sequencing_auxiliary_set)
    if value['assay_term']['term_name'] in ['proliferation CRISPR screen',
                                            'CRISPR perturbation screen followed by flow cytometry and FISH',
                                            'CRISPR perturbation screen followed by single-cell RNA sequencing']:
        auxiliary_sets = [system.get('request').embed(auxiliary_set['@id'], '@@object?skip_calculated=true')
                          for auxiliary_set in value.get('auxiliary_sets', '')]
        if not (auxiliary_sets) or not ([auxiliary_set for auxiliary_set in auxiliary_sets if auxiliary_set.get('file_set_type') == 'gRNA sequencing']):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has no gRNA sequencing `auxiliary_sets`.'
            )
            yield AuditFailure('missing auxiliary set', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='embedded')
def audit_Variant_FlowFISH_missing_variant_sequencing_auxiliary_set(value, system):
    '''
    [
        {
            "audit_description": "Variant FlowFISH measurement sets are expected to link to a variant sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_Variant_FlowFISH_missing_variant_sequencing_auxiliary_set)
    if value.get('preferred_assay_title') == 'Variant FlowFISH':
        auxiliary_sets = [system.get('request').embed(auxiliary_set['@id'], '@@object?skip_calculated=true')
                          for auxiliary_set in value.get('auxiliary_sets', '')]
        if not (auxiliary_sets) or not ([auxiliary_set for auxiliary_set in auxiliary_sets if auxiliary_set.get('file_set_type') == 'variant sequencing']):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has no variant sequencing `auxiliary_sets`.'
            )
            yield AuditFailure('missing auxiliary set', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='embedded')
def audit_CRISPR_assay_missing_cell_sorting_auxiliary_set(value, system):
    '''
    [
        {
            "audit_description": "CRISPR-based measurement sets that utilize flow cytometry are expected to link to a cell sorting auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_CRISPR_assay_missing_cell_sorting_auxiliary_set)
    assay_term_name = value.get('assay_term', {}).get('term_name')
    preferred_assay_title = value.get('preferred_assay_title', '')
    crispr_flow_assays = ['CRISPR perturbation screen followed by flow cytometry and FISH', 'Variant FlowFISH']
    if assay_term_name in crispr_flow_assays or preferred_assay_title in crispr_flow_assays:
        auxiliary_sets = [system.get('request').embed(auxiliary_set['@id'], '@@object?skip_calculated=true')
                          for auxiliary_set in value.get('auxiliary_sets', '')]
        if not (auxiliary_sets) or not ([auxiliary_set for auxiliary_set in auxiliary_sets if auxiliary_set.get('file_set_type') == 'cell sorting']):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has no cell sorting `auxiliary_sets`.'
            )
            yield AuditFailure('missing auxiliary set', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_missing_auxiliary_sets(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets are expected to link to auxiliary sets if they share the same sample.",
            "audit_category": "missing auxiliary set",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_missing_auxiliary_sets)
    samples = value.get('samples', [])
    auxiliary_sets = value.get('auxiliary_sets', [])
    for sample in samples:
        sample_object = system.get('request').embed(sample, '@@object')
        for file_set in sample_object.get('file_sets', []):
            if file_set.startswith('/auxiliary-sets/') and file_set not in auxiliary_sets:
                detail = (
                    f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} links '
                    f'to sample {audit_link(path_to_text(sample),sample)} which links to auxiliary set '
                    f'{audit_link(path_to_text(file_set),file_set)} but is not in its `auxiliary_sets`.'
                )
                yield AuditFailure('missing auxiliary set', f'{detail} {description}', level='WARNING')


@audit_checker('MeasurementSet', frame='object')
def audit_missing_auxiliary_set_MPRA(value, system):
    '''
    [
        {
            "audit_description": "MPRA measurement sets are expected to link to a quantification DNA barcode sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_missing_auxiliary_set_MPRA)
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name')
    if assay_term_name == 'massively parallel reporter assay':
        auxiliary_sets = [system.get('request').embed(auxiliary_set, '@@object?skip_calculated=true')
                          for auxiliary_set in value.get('auxiliary_sets', [])]
        if not (auxiliary_sets) or not ([auxiliary_set for auxiliary_set in auxiliary_sets if auxiliary_set.get('file_set_type', '') == 'quantification DNA barcode sequencing']):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has no quantification DNA barcode sequencing `auxiliary_sets`.'
            )
            yield AuditFailure('missing auxiliary set', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('MeasurementSet', frame='object')
def audit_targeted_genes(value, system):
    '''
    [
        {
            "audit_description": "ChIP-seq and FISH-based assays are expected to specify targeted gene(s).",
            "audit_category": "missing targeted genes",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Only ChIP-seq and FISH-based assays are expected to specify targeted gene(s).",
            "audit_category": "unexpected targeted genes",
            "audit_level": "WARNING"
        }
    ]
    '''
    description_missing = get_audit_description(audit_targeted_genes, index=0)
    description_unexpected = get_audit_description(audit_targeted_genes, index=1)
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name', '')
    targeted_genes = value.get('targeted_genes', '')
    preferred_assay_title = value.get('preferred_assay_title', '')
    expecting_targeted_genes_by_assay_term = ['CRISPR perturbation screen followed by flow cytometry and FISH',
                                              'ChIP-seq assay',
                                              'transcription factor binding site identification by ChIP-Seq assay',
                                              ]
    expecting_targeted_genes_by_preferred_assay_title = ['Variant FlowFISH']
    if not (targeted_genes) and (assay_term_name in expecting_targeted_genes_by_assay_term or preferred_assay_title in expecting_targeted_genes_by_preferred_assay_title):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has no `targeted_genes`.'
        )
        yield AuditFailure('missing targeted genes', f'{detail} {description_missing}', level='NOT_COMPLIANT')
    if targeted_genes and (assay_term_name not in expecting_targeted_genes_by_assay_term and preferred_assay_title not in expecting_targeted_genes_by_preferred_assay_title):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'has `targeted_genes`.'
        )
        yield AuditFailure('unexpected targeted genes', f'{detail} {description_unexpected}', level='WARNING')


@audit_checker('MeasurementSet', frame='embedded')
def audit_missing_construct_library_set(value, system):
    '''
    [
        {
            "audit_description": "MPRA measurement sets are expected to link to a construct library set of the type reporter library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "CRISPR-based assay measurement sets, with the exception of SGE, are expected to link to a construct library set of the type guide library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "SGE measurement sets are expected to link to a construct library set of the type editing template library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Protein-protein interaction detection assay measurement sets are expected to link to a construct library set of the type expression vector library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "VAMP-seq measurement sets are expected to link to a construct library set of the type expression vector library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Imaging assay measurement sets are expected to link to a construct library set of the type expression vector library in its samples.",
            "audit_category": "missing construct library set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description_MPRA = get_audit_description(audit_missing_construct_library_set, index=0)
    description_CRISPR = get_audit_description(audit_missing_construct_library_set, index=1)
    description_SGE = get_audit_description(audit_missing_construct_library_set, index=2)
    description_PPI = get_audit_description(audit_missing_construct_library_set, index=3)
    description_VAMP = get_audit_description(audit_missing_construct_library_set, index=4)
    description_Imaging = get_audit_description(audit_missing_construct_library_set, index=5)

    expected_library_by_assay_term = {
        'massively parallel reporter assay': ('reporter library', description_MPRA),
        'cas mediated mutagenesis': ('guide library', description_CRISPR),
        'proliferation CRISPR screen': ('guide library', description_CRISPR),
        'CRISPR perturbation screen followed by flow cytometry and FISH': ('guide library', description_CRISPR),
        'CRISPR perturbation screen followed by single-cell RNA sequencing': ('guide library', description_CRISPR),
        'protein-protein interaction detection assay': ('expression vector library', description_PPI),
        'imaging assay': ('expression vector library', description_Imaging)
    }
    # preferred assay title expectations override any overlapping assay term expectation
    expected_library_by_preferred_assay_title = {
        'SGE': ('editing template library', description_SGE),
        'VAMP-seq': ('expression vector library', description_VAMP)
    }

    assay_term_name = value.get('assay_term').get('term_name')
    preferred_assay_title = value.get('preferred_assay_title')
    construct_library_sets = value.get('samples')[0].get('construct_library_sets')

    if (assay_term_name in expected_library_by_assay_term or preferred_assay_title in expected_library_by_preferred_assay_title) and not (value.get('control_for')):

        if preferred_assay_title in expected_library_by_preferred_assay_title:
            expected_library_dict_to_check = expected_library_by_preferred_assay_title
            assay_to_check = preferred_assay_title
        else:
            expected_library_dict_to_check = expected_library_by_assay_term
            assay_to_check = assay_term_name

        expected_library = expected_library_dict_to_check[assay_to_check][0]
        description = expected_library_dict_to_check[assay_to_check][1]
        if not (construct_library_sets) or not ([construct_library_set for construct_library_set in construct_library_sets if construct_library_set.get('file_set_type', '') == expected_library]):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has no `construct_library_sets` of type {expected_library} linked in its `samples`.'
            )
            yield AuditFailure('missing construct library set', f'{detail} {description}', level='NOT_COMPLIANT')
