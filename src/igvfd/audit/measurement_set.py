from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)

from .file_set import (
    single_cell_check
)


@audit_checker('MeasurementSet', frame='object')
def audit_related_multiome_datasets(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets from multiome assays are expected to specify a multiome size.",
            "audit_category": "missing multiome size",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Only measurement sets from multiome assays are expected to specify a multiome size.",
            "audit_category": "unexpected multiome size",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Measurement sets with a multiome size are expected to have the corresponding amount of measurement sets (excluding itself) listed in related multiome datasets. Each of these datasets are expected to have the same multiome size and samples.",
            "audit_category": "inconsistent multiome datasets",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_no_multiome_size = get_audit_message(audit_related_multiome_datasets, index=0)
    audit_message_unexpected_multiome_size = get_audit_message(audit_related_multiome_datasets, index=1)
    audit_message_inconsistent_multiome = get_audit_message(audit_related_multiome_datasets, index=2)
    detail = ''
    related_multiome_datasets = value.get('related_multiome_datasets', [])
    multiome_size = value.get('multiome_size')
    preferred_assay_title = value.get('preferred_assay_title', '')
    if preferred_assay_title in ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq', '10x multiome with scMito-seq']:
        if not multiome_size:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has no `multiome_size`.'
            )
            yield AuditFailure(audit_message_no_multiome_size.get('audit_category', ''), f'{detail} {audit_message_no_multiome_size.get("audit_description", "")}', level=audit_message_no_multiome_size.get('audit_level', ''))
    else:
        if multiome_size:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has `multiome_size`.'
            )
            yield AuditFailure(audit_message_unexpected_multiome_size.get('audit_category', ''), f'{detail} {audit_message_unexpected_multiome_size.get("audit_description", "")}', level=audit_message_unexpected_multiome_size.get('audit_level', ''))
    if related_multiome_datasets == [] and multiome_size:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has a `multiome_size` of {multiome_size}, but no `related_multiome_datasets`.'
        )
        yield AuditFailure(audit_message_inconsistent_multiome.get('audit_category', ''), f'{detail} {audit_message_inconsistent_multiome.get("audit_description", "")}', level=audit_message_inconsistent_multiome.get('audit_level', ''))
    elif related_multiome_datasets and multiome_size:
        if len(related_multiome_datasets) != multiome_size - 1:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a `multiome_size` of {multiome_size}, but {len(related_multiome_datasets)} '
                f'`related_multiome_datasets` when {multiome_size - 1} are expected.'
            )
            yield AuditFailure(audit_message_inconsistent_multiome.get('audit_category', ''), f'{detail} {audit_message_inconsistent_multiome.get("audit_description", "")}', level=audit_message_inconsistent_multiome.get('audit_level', ''))
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
            yield AuditFailure(audit_message_inconsistent_multiome.get('audit_category', ''), f'{detail} {audit_message_inconsistent_multiome.get("audit_description", "")}', level=audit_message_inconsistent_multiome.get('audit_level', ''))
        if datasets_with_different_multiome_sizes:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a specified `multiome_size` of {multiome_size}, which does not match the '
                f'`multiome_size` of `related_multiome_datasets`: {datasets_with_different_multiome_sizes}'
            )
            yield AuditFailure(audit_message_inconsistent_multiome.get('audit_category', ''), f'{detail} {audit_message_inconsistent_multiome.get("audit_description", "")}', level=audit_message_inconsistent_multiome.get('audit_level', ''))


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
    audit_message = get_audit_message(audit_unspecified_protocol)
    if 'protocols' not in value:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `protocols`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    audit_message = get_audit_message(audit_CRISPR_screen_lacking_modifications)
    assay_term = value.get('assay_term')
    assay = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    crispr_assays = ['in vitro CRISPR screen assay',
                     'in vitro CRISPR screen using flow cytometry',
                     'in vitro CRISPR screen using single-cell RNA-seq'
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
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} is '
                f'a CRISPR screen assay but has no specified `modifications` on its `samples`: {sample_detail}.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_preferred_assay_title(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets are expected to specify an appropriate preferred assay title for its respective assay term.",
            "audit_category": "inconsistent preferred assay title",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_inconsistent = get_audit_message(audit_preferred_assay_title, index=0)
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name')
    preferred_assay_title = value.get('preferred_assay_title', '')
    if preferred_assay_title not in assay_object.get('preferred_assay_titles', []):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} has '
            f'`assay_term` {assay_term_name}, but `preferred_assay_title` {preferred_assay_title}.'
        )
        yield AuditFailure(audit_message_inconsistent.get('audit_category', ''), f'{detail} {audit_message_inconsistent.get("audit_description", "")}', level=audit_message_inconsistent.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_missing_institutional_certification(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets for mapping assays or controlled access characterization assays involving samples with a human origin are expected to link to the relevant institutional certificates.",
            "audit_category": "missing NIH certification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_missing_institutional_certification)
    # Only audit Measurement Sets with at least one human sample.
    donors = value.get('donors', [])
    taxa = set()
    for donor in donors:
        donor_obj = system.get('request').embed(donor, '@@object?skip_calculated=true')
        taxa.add(donor_obj.get('taxa', ''))
    if 'Homo sapiens' not in taxa:
        return

    # Characterization assays do not need to be audited if they do not have controlled access data.
    characterization_assays = [
        'OBI:0003133',  # cas mediated mutagenesis
        'OBI:0003659',  # in vitro CRISPR screen assay
        'OBI:0003661',  # in vitro CRISPR screen using flow cytometry
        'OBI:0003660',  # in vitro CRISPR screen using single-cell RNA-seq
        'OBI:0000916',  # flow cytometry assay
        'OBI:0000185',  # imaging assay
        'OBI:0002675',  # massively parallel reporter assay',
        'OBI:0000288',  # protein-protein interaction detection assay',
        'OBI:0002041'  # self-transcribing active regulatory region sequencing assay
    ]
    assay_term = value.get('assay_term', '')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_id = assay_object.get('term_id', '')
    files = [system.get('request').embed(file, '@@object?skip_calculated=true') for file in value.get('files', '')]
    if assay_term_id in characterization_assays and not (any([file.get('controlled_access') for file in files])):
        return

    lab = value.get('lab', '')
    award = value.get('award', '')
    samples = value.get('samples', [])

    sample_objects_to_check = []
    for sample in samples:
        sample_object = system.get('request').embed(sample, '@@object')
        if 'MultiplexedSample' in sample_object['@type']:
            multiplexed_sample_id = sample_object['@id']
            multiplexed_phrase = f' that is multiplexed in {audit_link(path_to_text(multiplexed_sample_id), multiplexed_sample_id)}'
            for mux_sample in sample_object['multiplexed_samples']:
                mux_sample_object = system.get('request').embed(mux_sample, '@@object')
                if any(donor.startswith('/human-donors/') for donor in mux_sample_object.get('donors', [])):
                    sample_objects_to_check.append((mux_sample_object, multiplexed_phrase))
        else:
            sample_objects_to_check.append((sample_object, ''))

    for sample_tuple in sample_objects_to_check:
        sample = sample_tuple[0]
        multiplexed_phrase = sample_tuple[1]
        nic_labs = []
        nic_awards = []
        for nic in sample.get('institutional_certificates', []):
            nic_object = system.get('request').embed(nic, '@@object?skip_calculated=true')
            nic_labs.append(nic_object.get('lab', ''))
            if 'partner_labs' in nic_object:
                for partner in nic_object.get('partner_labs', []):
                    nic_labs.append(partner)
            nic_awards.append(nic_object.get('award', ''))
            if 'partner_awards' in nic_object:
                for partner in nic_object.get('partner_awards', []):
                    nic_awards.append(partner)
        if lab not in nic_labs or award not in nic_awards:
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} has '
                f'a sample {audit_link(path_to_text(sample["@id"]), sample["@id"])}{multiplexed_phrase} '
                f'that lacks any `institutional_certificates` issued to the lab '
                f'that submitted this file set or to a partner lab/award of the submitting lab.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_missing_auxiliary_set_link(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets are expected to link to auxiliary sets if they share the same sample.",
            "audit_category": "missing auxiliary set",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message = get_audit_message(audit_missing_auxiliary_set_link)
    samples = value.get('samples', [])
    auxiliary_sets = value.get('auxiliary_sets', [])
    for sample in samples:
        sample_object = system.get('request').embed(sample, '@@object')
        for file_set in sample_object.get('file_sets', []):
            if file_set.startswith('/auxiliary-sets/') and file_set not in auxiliary_sets:
                auxiliary_set_object = system.get('request').embed(file_set, '@@object?skip_calculated=true')
                if auxiliary_set_object.get('status', '') in ['in progress', 'released', 'archived']:
                    detail = (
                        f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} links '
                        f'to sample {audit_link(path_to_text(sample), sample)} which links to auxiliary set '
                        f'{audit_link(path_to_text(file_set), file_set)} but is not in its `auxiliary_sets`.'
                    )
                    yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_targeted_genes(value, system):
    '''
    [
        {
            "audit_description": "ChIP-seq and CRISPR flow cytometry assays are expected to specify targeted gene(s).",
            "audit_category": "missing targeted genes",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "Only ChIP-seq and CRISPR flow cytometry assays are expected to specify targeted gene(s).",
            "audit_category": "unexpected targeted genes",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing = get_audit_message(audit_targeted_genes, index=0)
    audit_message_unexpected = get_audit_message(audit_targeted_genes, index=1)
    assay_term = value.get('assay_term')
    assay_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_object.get('term_name', '')
    targeted_genes = value.get('targeted_genes', '')
    preferred_assay_title = value.get('preferred_assay_title', '')
    expecting_targeted_genes_by_assay_term = ['in vitro CRISPR screen using flow cytometry',
                                              'ChIP-seq assay',
                                              'transcription factor binding site identification by ChIP-Seq assay',
                                              ]
    expecting_targeted_genes_by_preferred_assay_title = ['Variant-EFFECTS']
    if not (targeted_genes) and (assay_term_name in expecting_targeted_genes_by_assay_term or preferred_assay_title in expecting_targeted_genes_by_preferred_assay_title):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `targeted_genes`.'
        )
        yield AuditFailure(audit_message_missing.get('audit_category', ''), f'{detail} {audit_message_missing.get("audit_description", "")}', level=audit_message_missing.get('audit_level', ''))
    if targeted_genes and (assay_term_name not in expecting_targeted_genes_by_assay_term and preferred_assay_title not in expecting_targeted_genes_by_preferred_assay_title):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `targeted_genes`.'
        )
        yield AuditFailure(audit_message_unexpected.get('audit_category', ''), f'{detail} {audit_message_unexpected.get("audit_description", "")}', level=audit_message_unexpected.get('audit_level', ''))


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
    audit_message_MPRA = get_audit_message(audit_missing_construct_library_set, index=0)
    audit_message_CRISPR = get_audit_message(audit_missing_construct_library_set, index=1)
    audit_message_SGE = get_audit_message(audit_missing_construct_library_set, index=2)
    audit_message_PPI = get_audit_message(audit_missing_construct_library_set, index=3)
    audit_message_VAMP = get_audit_message(audit_missing_construct_library_set, index=4)
    audit_message_Imaging = get_audit_message(audit_missing_construct_library_set, index=5)

    expected_library_by_assay_term = {
        'massively parallel reporter assay': ('reporter library', audit_message_MPRA),
        'cas mediated mutagenesis': ('guide library', audit_message_CRISPR),
        'in vitro CRISPR screen assay': ('guide library', audit_message_CRISPR),
        'in vitro CRISPR screen using flow cytometry': ('guide library', audit_message_CRISPR),
        'in vitro CRISPR screen using single-cell RNA-seq': ('guide library', audit_message_CRISPR),
        'protein-protein interaction detection assay': ('expression vector library', audit_message_PPI),
        'imaging assay': ('expression vector library', audit_message_Imaging)
    }
    # preferred assay title expectations override any overlapping assay term expectation
    expected_library_by_preferred_assay_title = {
        'SGE': ('editing template library', audit_message_SGE),
        'VAMP-seq': ('expression vector library', audit_message_VAMP),
        'VAMP-seq (MultiSTEP)': ('expression vector library', audit_message_VAMP)
    }

    assay_term_name = value.get('assay_term').get('term_name')
    preferred_assay_title = value.get('preferred_assay_title')
    construct_library_sets = value.get('construct_library_sets')

    if (assay_term_name in expected_library_by_assay_term or preferred_assay_title in expected_library_by_preferred_assay_title) and not (value.get('control_for')):

        if preferred_assay_title in expected_library_by_preferred_assay_title:
            expected_library_dict_to_check = expected_library_by_preferred_assay_title
            assay_to_check = preferred_assay_title
        else:
            expected_library_dict_to_check = expected_library_by_assay_term
            assay_to_check = assay_term_name

        expected_library = expected_library_dict_to_check[assay_to_check][0]
        audit_message = expected_library_dict_to_check[assay_to_check][1]
        if not (construct_library_sets) or not ([construct_library_set for construct_library_set in construct_library_sets if construct_library_set.get('file_set_type', '') == expected_library]):
            detail = (
                f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has no `construct_library_sets` of type {expected_library} linked in its `samples`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='embedded')
def audit_missing_auxiliary_set(value, system):
    '''
    [
        {
            "audit_description": "MPRA measurement sets are expected to link to a quantification DNA barcode sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "scQer MPRA measurement sets are expected to link to a circularized RNA barcode detection auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Single-cell CRISPR screens, such as Perturb-seq, are expected to link to a gRNA sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "CRISPR-based measurement sets that utilize flow cytometry are expected to link to a cell sorting auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "10X Multiome MULTI-seq measurement sets are expected to link to a lipid-conjugated oligo sequencing auxiliary set.",
            "audit_category": "missing auxiliary set",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message_MPRA = get_audit_message(audit_missing_auxiliary_set, index=0)
    audit_message_scQer = get_audit_message(audit_missing_auxiliary_set, index=1)
    audit_message_scCRISPR_gRNA = get_audit_message(audit_missing_auxiliary_set, index=2)
    audit_message_CRISPR_flow = get_audit_message(audit_missing_auxiliary_set, index=3)
    audit_message_10X_MULTI_seq = get_audit_message(audit_missing_auxiliary_set, index=4)

    expected_auxiliary_set_by_assay_term = {
        'massively parallel reporter assay': [('quantification DNA barcode sequencing', audit_message_MPRA)],
        'in vitro CRISPR screen using flow cytometry': [('cell sorting', audit_message_CRISPR_flow)],
        'in vitro CRISPR screen using single-cell RNA-seq': [('gRNA sequencing', audit_message_scCRISPR_gRNA)]
    }
    # preferred assay title expectations override any overlapping assay term expectation
    expected_auxiliary_set_by_preferred_assay_title = {
        'MPRA (scQer)': [('quantification DNA barcode sequencing', audit_message_MPRA), ('circularized RNA barcode detection', audit_message_scQer)],
        '10x multiome with MULTI-seq': [('lipid-conjugated oligo sequencing', audit_message_10X_MULTI_seq)]
    }

    assay_term_name = value.get('assay_term').get('term_name')
    preferred_assay_title = value.get('preferred_assay_title')
    auxiliary_sets = value.get('auxiliary_sets')

    if (assay_term_name in expected_auxiliary_set_by_assay_term or preferred_assay_title in expected_auxiliary_set_by_preferred_assay_title):

        if preferred_assay_title in expected_auxiliary_set_by_preferred_assay_title:
            expected_auxiliary_dict_to_check = expected_auxiliary_set_by_preferred_assay_title
            assay_to_check = preferred_assay_title
        else:
            expected_auxiliary_dict_to_check = expected_auxiliary_set_by_assay_term
            assay_to_check = assay_term_name

        expected_auxiliary_sets = expected_auxiliary_dict_to_check[assay_to_check]
        for expected_auxiliary_set in expected_auxiliary_sets:
            expected_auxiliary_set_type = expected_auxiliary_set[0]
            audit_message = expected_auxiliary_set[1]

            if not (auxiliary_sets) or not ([auxiliary_set for auxiliary_set in auxiliary_sets if auxiliary_set.get('file_set_type', '') == expected_auxiliary_set_type]):
                detail = (
                    f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'has no {expected_auxiliary_set_type} `auxiliary_sets`.'
                )
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='embedded')
def audit_missing_strand_specificity(value, system):
    '''
    [
        {
            "audit_description": "Single-cell CRISPR screens, such as Perturb-seq, scCRISPR screen, TAP-seq, and CERES-seq, are expected to specify strand specificity.",
            "audit_category": "missing strand specificity",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message_strand_specificity = get_audit_message(audit_missing_strand_specificity)

    expected_assays = {'Perturb-seq', 'scCRISPR screen', 'TAP-seq', 'CERES-seq'}
    preferred_assay_title = value.get('preferred_assay_title')
    strand_specificity = value.get('strand_specificity')

    if preferred_assay_title in expected_assays and strand_specificity is None:
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'is missing required `strand_specificity` for assay {preferred_assay_title}.'
        )
        yield AuditFailure(
            audit_message_strand_specificity.get('audit_category', ''),
            f'{detail} {audit_message_strand_specificity.get("audit_description", "")}',
            level=audit_message_strand_specificity.get('audit_level', '')
        )


@audit_checker('MeasurementSet', frame='object')
def audit_onlist(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets to be processed via the single cell uniform pipeline are expected to have onlist files and onlist methods indicated.",
            "audit_category": "missing barcode onlist",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Measurement sets not intended for the single cell uniform pipeline are expected not to have onlist files or onlist methods.",
            "audit_category": "unexpected barcode onlist",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing_all_onlist_info = get_audit_message(audit_onlist, index=0)
    audit_message_unwanted_onlist_info = get_audit_message(audit_onlist, index=1)
    onlist_files = value.get('onlist_files')
    onlist_method = value.get('onlist_method')
    assay_term = value.get('assay_term')
    assay_term_obj = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
    assay_term_name = assay_term_obj.get('term_name', '')
    single_cell_assay_status = single_cell_check(system, value, 'Measurement set')
    # Check if single cell assays MeaSets are missing both onlist files and methods
    if (single_cell_assay_status) and (not onlist_method) and (not onlist_files):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has an `assay_term` of {assay_term_name} but no `onlist_files` nor `onlist_methods`.'
        )
        yield AuditFailure(audit_message_missing_all_onlist_info.get('audit_category', ''),
                           f'{detail} {audit_message_missing_all_onlist_info.get("audit_description", "")}',
                           level=audit_message_missing_all_onlist_info.get('audit_level', '')
                           )
    # Check if non-single cell MeaSets have onlist methods and files
    if (not single_cell_assay_status) and (onlist_method) and (onlist_files):
        detail = (
            f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has an `assay_term` of {assay_term_name} but has `onlist_files` and `onlist_method`.'
        )
        yield AuditFailure(audit_message_unwanted_onlist_info.get('audit_category', ''),
                           f'{detail} {audit_message_unwanted_onlist_info.get("audit_description", "")}',
                           level=audit_message_unwanted_onlist_info.get('audit_level', '')
                           )


@audit_checker('MeasurementSet', frame='object')
def audit_inconsistent_onlist_info(value, system):
    '''
    [
        {
            "audit_description": "Measurement sets with 2 or more barcode onlist files are expected to have an onlist method of either product or multi.",
            "audit_category": "inconsistent barcode onlist",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing_method_mismatch_combo = get_audit_message(audit_inconsistent_onlist_info, index=0)
    onlist_files = value.get('onlist_files')
    onlist_method = value.get('onlist_method')
    # Only check if both files and method properties are present
    if onlist_files and onlist_method:
        # Check if multiple onlist files are submitted but the method is no combination
        if (len(onlist_files) > 1) and (onlist_method == 'no combination'):
            yield AuditFailure(audit_message_missing_method_mismatch_combo.get('audit_category', ''), audit_message_missing_method_mismatch_combo.get('audit_description', ''), level=audit_message_missing_method_mismatch_combo.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_unexpected_onlist_content(value, system):
    '''
    [
        {
            "audit_description": "Onlist files are expected to be tabular files with barcode onlist as the content type.",
            "audit_category": "unexpected onlist files",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_unexpected_onlist_content = get_audit_message(audit_unexpected_onlist_content, index=0)
    onlist_files = value.get('onlist_files')
    # If onlist files exist, check if the content type is NOT barcode onlist.
    if onlist_files:
        for onlist_file in onlist_files:
            if onlist_file.startswith('/tabular-files/'):
                file_obj = system.get('request').embed(onlist_file, '@@object?skip_calculated=true')
                if file_obj.get('content_type', '') != 'barcode onlist':
                    details = (
                        f'The `onlist_files` {audit_link(path_to_text(onlist_file), onlist_file)} '
                        f'is expected to have barcode onlist as the `content_type`.'
                    )
                    yield AuditFailure(audit_message_unexpected_onlist_content.get('audit_category', ''),
                                       f'{details} {audit_message_unexpected_onlist_content.get("audit_description", "")}',
                                       level=audit_message_unexpected_onlist_content.get('audit_level', '')
                                       )
