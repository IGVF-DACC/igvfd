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
    single_cell_check,
    TRANSCRIPT_ASSAY_TERMS
)


def get_assay_terms(value, system):
    assay_terms = set()
    for input_file_set in value.get('input_file_sets', []):
        if input_file_set.startswith('/measurement-sets/'):
            input_file_set_object = system.get('request').embed(input_file_set + '@@object?skip_calculated=true')
            assay_terms.add(input_file_set_object.get('assay_term'))
    return list(assay_terms)


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_multiplexed_samples(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets with multiplexed samples are expected to specify a demultiplexed sample.",
            "audit_category": "missing demultiplexed sample",
            "audit_level": "INTERNAL_ACTION"
        },
        {
            "audit_description": "Analysis sets are only expected to specify a demultiplexed sample if it has samples and they are all multiplexed.",
            "audit_category": "unexpected demultiplexed sample",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Analysis sets are expected to specify only multiplexed or non-multiplexed samples, not both.",
            "audit_category": "unexpected samples",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Analysis sets are expected to specify a demultiplexed sample that was multiplexed in a multiplexed sample associated with an input file set.",
            "audit_category": "inconsistent demultiplexed sample",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing_demultiplexed_from = get_audit_message(audit_analysis_set_multiplexed_samples, index=0)
    audit_message_unexpected_demultiplexed_from = get_audit_message(audit_analysis_set_multiplexed_samples, index=1)
    audit_message_unexpected_samples = get_audit_message(audit_analysis_set_multiplexed_samples, index=2)
    audit_message_inconsistent_demultiplexed_sample = get_audit_message(audit_analysis_set_multiplexed_samples, index=3)
    samples = value.get('samples', [])
    demultiplexed_sample = value.get('demultiplexed_sample', '')
    multiplexed_samples = [sample for sample in samples if sample.startswith('/multiplexed-samples/')]
    multiplexed_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                     for sample in multiplexed_samples])
    non_multiplexed_samples = [sample for sample in samples if not (sample.startswith('/multiplexed-samples/'))]
    non_multiplexed_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                        for sample in non_multiplexed_samples])
    if not (demultiplexed_sample) and multiplexed_samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `input_file_sets` with multiplexed samples: {multiplexed_samples} '
            f'but no `demultiplexed_sample`.'
        )
        yield AuditFailure(audit_message_missing_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_missing_demultiplexed_from.get("audit_description", "")}', level=audit_message_missing_demultiplexed_from.get('audit_level', ''))
    if demultiplexed_sample and non_multiplexed_samples and [demultiplexed_sample] != samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has a `demultiplexed_sample` and non-multiplexed '
            f'`samples`: {non_multiplexed_samples}.'
        )
        yield AuditFailure(audit_message_unexpected_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_unexpected_demultiplexed_from.get("audit_description", "")}', level=audit_message_unexpected_demultiplexed_from.get('audit_level', ''))
    if demultiplexed_sample and not (samples):
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has a `demultiplexed_sample` and no `samples`. '
        )
        yield AuditFailure(audit_message_unexpected_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_unexpected_demultiplexed_from.get("audit_description", "")}', level=audit_message_unexpected_demultiplexed_from.get('audit_level', ''))
    if multiplexed_samples and non_multiplexed_samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has multiplexed samples: {multiplexed_samples} and non-multiplexed '
            f'samples: {non_multiplexed_samples}.'
        )
        yield AuditFailure(audit_message_unexpected_samples.get('audit_category', ''), f'{detail} {audit_message_unexpected_samples.get("audit_description", "")}', level=audit_message_unexpected_samples.get('audit_level', ''))
    if demultiplexed_sample and samples and [demultiplexed_sample] == samples:
        input_file_sets = value.get('input_file_sets', [])
        all_multiplexed_samples = set()
        all_samples = []
        for input_file_set in input_file_sets:
            input_file_set_object = system.get('request').embed(input_file_set + '@@object')
            input_samples = input_file_set_object.get('samples')
            for sample in input_samples:
                all_samples.append(sample)
                sample_object = system.get('request').embed(sample + '@@object')
                all_multiplexed_samples = all_multiplexed_samples | set(sample_object.get('multiplexed_samples', []))
        all_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                 for sample in all_samples])
        input_file_sets = ', '.join([audit_link(path_to_text(input_file_set), input_file_set)
                                    for input_file_set in input_file_sets])
        if demultiplexed_sample not in all_multiplexed_samples:
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a `demultiplexed_sample` that is not represented in the `multiplexed_samples` '
                f'of the `samples`: {all_samples} of its `input_file_sets`: {input_file_sets}.'
            )
            yield AuditFailure(audit_message_inconsistent_demultiplexed_sample.get('audit_category', ''), f'{detail} {audit_message_inconsistent_demultiplexed_sample.get("audit_description", "")}', level=audit_message_inconsistent_demultiplexed_sample.get('audit_level', ''))


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_inconsistent_onlist_info(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets to be processed by the single cell uniform pipeline runs are expected to have the same onlist files for input measurement sets of the same assay.",
            "audit_category": "inconsistent barcode onlists",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "Analysis sets to be processed by the single cell uniform pipeline runs are expected to have the same onlist methods for input measurement sets of the same assay.",
            "audit_category": "inconsistent barcode method",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_msg_inconsistent_onlist_files = get_audit_message(audit_analysis_set_inconsistent_onlist_info, index=0)
    audit_msg_inconsistent_onlist_method = get_audit_message(audit_analysis_set_inconsistent_onlist_info, index=1)
    onlist_files_by_assays = {}
    onlist_methods_by_assays = {}
    input_file_sets = value.get('input_file_sets', [])
    for input_file_set in input_file_sets:
        if input_file_set.startswith('/measurement-sets/'):
            input_file_set_object = system.get('request').embed(input_file_set + '@@object?skip_calculated=true')
            # Only check if single cell
            single_cell_assay_status = single_cell_check(system, input_file_set_object, 'Measurement set')
            if single_cell_assay_status:
                assay_term = input_file_set_object.get('assay_term', '')
                # Onlist files are lists
                onlist_files_by_assays.setdefault(assay_term, []).append(input_file_set_object.get('onlist_files', ''))
                # Onlist methods are str
                onlist_methods_by_assays.setdefault(assay_term, set()).add(
                    input_file_set_object.get('onlist_method', ''))

    # If there are multiple onlist methods from the input measurement sets of the same assay type, trigger audit
    for assay_term, onlist_methods in onlist_methods_by_assays.items():
        if len(onlist_methods) > 1:
            assay_term_obj = system.get('request').embed(assay_term + '@@object?skip_calculated=true')
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has Measurement set(s) with assay term: {assay_term_obj.get("term_name", "")} '
                f'with inconsistent `onlist_methods`.'
            )
            yield AuditFailure(audit_msg_inconsistent_onlist_method.get('audit_category', ''), f'{detail} {audit_msg_inconsistent_onlist_method.get("audit_description", "")}', level=audit_msg_inconsistent_onlist_method.get('audit_level', ''))

    # If the input measurement sets have different onlist files
    for assay_term, onlist_files in onlist_files_by_assays.items():
        if not all(set(sublist) == set(onlist_files[0]) for sublist in onlist_files):
            assay_term_obj = system.get('request').embed(assay_term + '@@object?skip_calculated=true')
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has Measurement set(s) with assay term: {assay_term_obj.get("term_name", "")} '
                f'with inconsistent `onlist_files`.'
            )
            yield AuditFailure(audit_msg_inconsistent_onlist_files.get('audit_category', ''), f'{detail} {audit_msg_inconsistent_onlist_files.get("audit_description", "")}', level=audit_msg_inconsistent_onlist_files.get('audit_level', ''))


@audit_checker('AnalysisSet', frame='object')
def audit_missing_transcriptome(value, system):
    '''
    [
        {
            "audit_description": "Analysis set files processed from transcript sequence data are expected to link to a transcriptome reference.",
            "audit_category": "missing reference files",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message = get_audit_message(audit_missing_transcriptome, index=0)
    assay_terms = get_assay_terms(value, system)
    files_missing_transcriptome = []
    if any(assay_term in TRANSCRIPT_ASSAY_TERMS for assay_term in assay_terms):
        files = value.get('files', [])
        if files:
            for file in files:
                if file.startswith(('/alignment-files/', '/matrix-files/', '/signal-files/')):
                    file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
                    reference_files = file_object.get('reference_files', [])
                    if reference_files:
                        has_transcriptome = False
                        for reference_file in reference_files:
                            reference_file_object = system.get('request').embed(
                                reference_file + '@@object?skip_calculated=true')
                            if reference_file_object.get('content_type', '') in ['transcriptome reference', 'transcriptome index']:
                                has_transcriptome = True
                        if not (has_transcriptome):
                            files_missing_transcriptome.append(file)
                    else:
                        files_missing_transcriptome.append(file)
    if files_missing_transcriptome:
        files_missing_transcriptome = ', '.join([audit_link(path_to_text(file), file)
                                                for file in files_missing_transcriptome])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has file(s) with no transcriptome `reference_files`: {files_missing_transcriptome} '
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('AnalysisSet', frame='object')
def audit_multiple_barcode_replacement_files_in_input(value, system):
    '''
    [
        {
            "audit_description": "All input Parse SPLiT-seq measurement sets linked to the same analysis set are expected to have the same barcode replacement file.",
            "audit_category": "unexpected barcode replacement file",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_msg_unexpected_file = get_audit_message(audit_multiple_barcode_replacement_files_in_input, index=0)
    barcode_replacement_files = set()
    parse_splitseq_file_sets = []
    if value.get('input_file_sets'):
        for file in value.get('input_file_sets'):
            if file.startswith('/measurement-sets/'):
                input_file_set_object = system.get('request').embed(file + '@@object?skip_calculated=true')
                assay_term = input_file_set_object.get('preferred_assay_title')
                if assay_term == 'Parse SPLiT-seq':
                    barcode_replacement_file = input_file_set_object.get('barcode_replacement_file', '')
                    # Only append replacement files that are not empty (or else it will result in a None value downstream)
                    if barcode_replacement_file:
                        barcode_replacement_files.add(barcode_replacement_file)
                        parse_splitseq_file_sets.append(file)
    # Audit 1: If all input Parse measurement sets have different barcode replacement files, trigger audit
    if len(barcode_replacement_files) > 1:
        barcode_replacement_files_links = ', '.join(
            [audit_link(path_to_text(tab_file), tab_file) for tab_file in barcode_replacement_files])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `input_file_sets` with `preferred_assay_title` Parse SPLiT-seq that are linked to different `barcode_replacement_file`s: {barcode_replacement_files_links}.'
        )
        yield AuditFailure(audit_msg_unexpected_file.get('audit_category', ''), f'{detail} {audit_msg_unexpected_file.get("audit_description", "")}', level=audit_msg_unexpected_file.get('audit_level', ''))
