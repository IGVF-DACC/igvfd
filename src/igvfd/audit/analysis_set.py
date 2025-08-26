from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    join_obj_paths
)

from .file_set import (
    single_cell_check,
    TRANSCRIPT_ASSAY_TERMS
)

from typing import Iterable


def get_assay_terms(value, system):
    assay_terms = set()
    for input_file_set in value.get('input_file_sets', []):
        if input_file_set.startswith('/measurement-sets/'):
            input_file_set_object = system.get('request').embed(input_file_set + '@@object?skip_calculated=true')
            assay_terms.add(input_file_set_object.get('assay_term'))
    return list(assay_terms)


def yield_all_upstream_seqfiles(file, system) -> Iterable[str]:
    '''
    Traverse recursively from Analysis set files upstream via derived_from until sequence files.

    Args:
        file (_type_): file type+accession, e.g. '/alignment-files/ENCFF123ABC'
        system (_type_): _description_

    Returns:
        Iterable[str]: SeqFiles

    Yields:
        Iterator[Iterable[str]]: SeqFiles
    '''
    if file.startswith('/sequence-files/'):
        yield file
        return
    file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
    for dfile in file_object.get('derived_from', []):
        yield from yield_all_upstream_seqfiles(dfile, system)


def check_genome_or_transcriptome_reference(file, system, reference_type) -> bool:
    '''Check if the file has a transcriptome reference.

    Args:
        file (str): file type+accession, e.g. '/alignment-files/ENCFF123ABC'
        system (_type_): _description_

    Returns:
        bool: True if transcriptome reference exists, False otherwise.
    '''
    if reference_type == 'transcriptome':
        expected_content_types = ['transcriptome reference', 'transcriptome index']
    elif reference_type == 'genome':
        expected_content_types = ['genome reference']
    file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
    reference_files = file_object.get('reference_files', [])
    ref_file_objects = []
    if reference_files:
        ref_file_objects = [system.get('request').embed(reference_file + '@@object?skip_calculated=true')
                            for reference_file in reference_files]
    return any(ref_file_object.get('content_type') in expected_content_types for ref_file_object in ref_file_objects)


def check_transcriptome_assay(file, system) -> bool:
    '''Check if the sequence file is linked to a Measurement Set of a transcriptome assay.

    Args:
        file (_type_): file type+accession, e.g. '/sequence-files/ENCFF123ABC'
        system (_type_): _description_

    Returns:
        bool: If linked to a transcriptome assay, return True, otherwise False.
    '''
    seqfile_object = system.get('request').embed(file + '@@object?skip_calculated=true')
    seqfile_fileset_object = system.get('request').embed(
        seqfile_object.get('file_set', '') + '@@object?skip_calculated=true')
    # assay_term is only on measurement set for now, still spelling it out explicitly
    assay_term = seqfile_fileset_object.get('assay_term', '')
    if assay_term:
        return assay_term in TRANSCRIPT_ASSAY_TERMS
    else:
        return False


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
    demultiplexed_samples = value.get('demultiplexed_samples', [])
    multiplexed_samples = [sample for sample in samples if sample.startswith('/multiplexed-samples/')]
    multiplexed_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                     for sample in multiplexed_samples])
    non_multiplexed_samples = [sample for sample in samples if not (sample.startswith('/multiplexed-samples/'))]
    non_multiplexed_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                        for sample in non_multiplexed_samples])
    if not (demultiplexed_samples) and multiplexed_samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `input_file_sets` with multiplexed samples: {multiplexed_samples} '
            f'but no `demultiplexed_samples`.'
        )
        yield AuditFailure(audit_message_missing_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_missing_demultiplexed_from.get("audit_description", "")}', level=audit_message_missing_demultiplexed_from.get('audit_level', ''))
    if demultiplexed_samples and non_multiplexed_samples and [demultiplexed_samples] != samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `demultiplexed_samples` and non-multiplexed '
            f'`samples`: {non_multiplexed_samples}.'
        )
        yield AuditFailure(audit_message_unexpected_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_unexpected_demultiplexed_from.get("audit_description", "")}', level=audit_message_unexpected_demultiplexed_from.get('audit_level', ''))
    if demultiplexed_samples and not (samples):
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `demultiplexed_samples` and no `samples`.'
        )
        yield AuditFailure(audit_message_unexpected_demultiplexed_from.get('audit_category', ''), f'{detail} {audit_message_unexpected_demultiplexed_from.get("audit_description", "")}', level=audit_message_unexpected_demultiplexed_from.get('audit_level', ''))
    if multiplexed_samples and non_multiplexed_samples:
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has multiplexed samples: {multiplexed_samples} and non-multiplexed '
            f'samples: {non_multiplexed_samples}.'
        )
        yield AuditFailure(audit_message_unexpected_samples.get('audit_category', ''), f'{detail} {audit_message_unexpected_samples.get("audit_description", "")}', level=audit_message_unexpected_samples.get('audit_level', ''))
    if demultiplexed_samples and samples and demultiplexed_samples == samples:
        input_file_sets = value.get('input_file_sets', [])
        all_multiplexed_samples = set()
        all_samples = []
        for input_file_set in input_file_sets:
            input_file_set_object = system.get('request').embed(input_file_set + '@@object')
            input_samples = input_file_set_object.get('samples', [])
            for sample in input_samples:
                all_samples.append(sample)
                sample_object = system.get('request').embed(sample + '@@object')
                all_multiplexed_samples = all_multiplexed_samples | set(sample_object.get('multiplexed_samples', []))
        all_samples = ', '.join([audit_link(path_to_text(sample), sample)
                                 for sample in all_samples])
        input_file_sets = ', '.join([audit_link(path_to_text(input_file_set), input_file_set)
                                    for input_file_set in input_file_sets])
        if any(demux_sample not in all_multiplexed_samples for demux_sample in demultiplexed_samples):
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has a sample in `demultiplexed_samples` that is not represented in the `multiplexed_samples` '
                f'of the `samples`: {all_samples} of its `input_file_sets`: {input_file_sets}.'
            )
            yield AuditFailure(audit_message_inconsistent_demultiplexed_sample.get('audit_category', ''), f'{detail} {audit_message_inconsistent_demultiplexed_sample.get("audit_description", "")}', level=audit_message_inconsistent_demultiplexed_sample.get('audit_level', ''))


def audit_analysis_set_inconsistent_onlist_info(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets to be processed by the single cell and perturb-seq uniform pipeline runs are expected to have the same onlist files for input measurement sets of the same assay.",
            "audit_category": "inconsistent barcode onlists",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "Analysis sets to be processed by the single cell and perturb-seq uniform pipeline runs are expected to have the same onlist methods for input measurement sets of the same assay.",
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
            input_file_set_object = system.get('request').embed(
                input_file_set + '@@object_with_select_calculated_properties?&field=assay_titles')
            # Skip assay if it's not single cell
            if not single_cell_check(system, input_file_set_object, 'Measurement set', include_perturb_seq=True):
                continue

            assay_titles = input_file_set_object.get('assay_titles', [])
            for assay_title in assay_titles:
                # Onlist files are lists
                onlist_files_by_assays.setdefault(assay_title, []).append(
                    input_file_set_object.get('onlist_files', [])
                )
                # Onlist methods are str
                onlist_methods_by_assays.setdefault(assay_title, set()).add(
                    input_file_set_object.get('onlist_method', '')
                )
    # If there are multiple onlist methods from the input measurement sets of the same assay type, trigger audit

    for assay_title, onlist_methods in onlist_methods_by_assays.items():
        if len(onlist_methods) > 1:
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has Measurement set(s) with assay title "{assay_title}" that have inconsistent `onlist_methods`.'
            )
            yield AuditFailure(
                audit_msg_inconsistent_onlist_method.get('audit_category', ''),
                f'{detail} {audit_msg_inconsistent_onlist_method.get("audit_description", "")}',
                level=audit_msg_inconsistent_onlist_method.get('audit_level', '')
            )

    # If the input measurement sets have different onlist files
    for assay_title, onlist_files in onlist_files_by_assays.items():
        if len(onlist_files) > 1 and not all(set(files) == set(onlist_files[0]) for files in onlist_files):
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has Measurement set(s) with assay title "{assay_title}" that have inconsistent `onlist_files`.'
            )
            yield AuditFailure(
                audit_msg_inconsistent_onlist_files.get('audit_category', ''),
                f'{detail} {audit_msg_inconsistent_onlist_files.get("audit_description", "")}',
                level=audit_msg_inconsistent_onlist_files.get('audit_level', '')
            )


def audit_missing_genome_transcriptome_references(value, system):
    '''
    [
        {
            "audit_description": "Analysis set files processed from transcript sequence data are expected to link to a transcriptome reference.",
            "audit_category": "missing reference files",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Analysis set files that contain genomic coordinates or refer to variants are expected to link to a genome reference.",
            "audit_category": "missing reference files",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Analysis set tabular files processed from transcript sequence data are expected to link to a transcriptome reference.",
            "audit_category": "missing reference files",
            "audit_level": "INTERNAL_ACTION"
        },
        {
            "audit_description": "Analysis set tabular files that contain genomic coordinates or refer to variants are expected to link to a genome reference.",
            "audit_category": "missing reference files",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    audit_message_transcriptome = get_audit_message(audit_missing_genome_transcriptome_references, index=0)
    audit_message_genome = get_audit_message(audit_missing_genome_transcriptome_references, index=1)
    audit_message_transcriptome_tabular = get_audit_message(audit_missing_genome_transcriptome_references, index=2)
    audit_message_genome_tabular = get_audit_message(audit_missing_genome_transcriptome_references, index=3)
    files = value.get('files', [])
    files_missing_genome = []  # List of files missing genome reference
    files_missing_transcriptome = []   # List of files missing transcriptome reference
    tabular_files_missing_genome = []  # List of tabular files missing genome reference
    tabular_files_missing_transcriptome = []   # List of tabular files missing transcriptome reference
    excluded_content_types_tabular_files = [
        'barcode onlist',
        'barcode replacement',
        'barcode to hashtag mapping',
        'barcode to sample mapping',
        'cell hashing barcodes',
        'derived barcode mapping',
        'external source data',
        'pipeline inputs',
        'primer sequences',
        'protein to protein interaction score',
        'sample sort parameters',
        'tissue positions'
    ]
    if files:
        for file in files:
            if not file.startswith(('/alignment-files/', '/matrix-files/', '/signal-files/', '/tabular-files/')):
                continue
            # Skip tabular files with certain excluded content_types.
            if file.startswith('/tabular-files/'):
                file_obj = system.get('request').embed(file + '@@object?skip_calculated=true')
                if file_obj['content_type'] in excluded_content_types_tabular_files:
                    continue
            # Get all upstream Seqfiles that eventually lead to data file
            # and check if upstream seqfiles are transcriptome based assays
            is_transcriptome_assay = any(
                check_transcriptome_assay(seq_file, system)
                for seq_file in yield_all_upstream_seqfiles(file, system)
            )
            # Check for genome reference.
            has_genome_reference = check_genome_or_transcriptome_reference(file, system, 'genome')
            # Check if the data file under the Analysis Set has a transcriptome reference
            has_transcriptome_reference = check_genome_or_transcriptome_reference(file, system, 'transcriptome')

            if not has_genome_reference:
                if file.startswith('/tabular-files/'):
                    tabular_files_missing_genome.append(file)
                else:
                    files_missing_genome.append(file)
            # If a transcriptome seqfile doesn't have transcriptome reference, add it to the list
            if is_transcriptome_assay and not has_transcriptome_reference:
                if file.startswith('/tabular-files/'):
                    tabular_files_missing_transcriptome.append(file)
                else:
                    files_missing_transcriptome.append(file)
    # Audit 1: if there are transcriptome based analysis files missing transcriptome references
    if files_missing_transcriptome:
        files_missing_transcriptome = join_obj_paths(data_object_paths=files_missing_transcriptome)
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has file(s) with no transcriptome `reference_files`: {files_missing_transcriptome}.'
        )
        yield AuditFailure(audit_message_transcriptome.get('audit_category', ''), f'{detail} {audit_message_transcriptome.get("audit_description", "")}', level=audit_message_transcriptome.get('audit_level', ''))

    # Audit 2: if there are genome based analysis files missing genome references
    if files_missing_genome:
        files_missing_genome = join_obj_paths(data_object_paths=files_missing_genome)
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has file(s) with no genome `reference_files`: {files_missing_genome}.'
        )
        yield AuditFailure(audit_message_genome.get('audit_category', ''), f'{detail} {audit_message_genome.get("audit_description", "")}', level=audit_message_genome.get('audit_level', ''))

    # Audit 3: if there are transcriptome based analysis tabular files missing transcriptome references
    if tabular_files_missing_transcriptome:
        tabular_files_missing_transcriptome = join_obj_paths(data_object_paths=tabular_files_missing_transcriptome)
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has tabular file(s) with no transcriptome `reference_files`: {tabular_files_missing_transcriptome}.'
        )
        yield AuditFailure(audit_message_transcriptome_tabular.get('audit_category', ''), f'{detail} {audit_message_transcriptome_tabular.get("audit_description", "")}', level=audit_message_transcriptome_tabular.get('audit_level', ''))

    # Audit 2: if there are genome based analysis files missing genome references
    if tabular_files_missing_genome:
        tabular_files_missing_genome = join_obj_paths(data_object_paths=tabular_files_missing_genome)
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has tabular file(s) with no genome `reference_files`: {tabular_files_missing_genome}.'
        )
        yield AuditFailure(audit_message_genome_tabular.get('audit_category', ''), f'{detail} {audit_message_genome_tabular.get("audit_description", "")}', level=audit_message_genome_tabular.get('audit_level', ''))


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
    for file in value.get('input_file_sets', []):
        if file.startswith('/measurement-sets/'):
            input_file_set_object = system.get('request').embed(file + '@@object?skip_calculated=true')
            preferred_assay_titles = input_file_set_object.get('preferred_assay_titles')
            if 'Parse SPLiT-seq' in preferred_assay_titles:
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
            f'has `input_file_sets` with `preferred_assay_titles` Parse SPLiT-seq that are linked to different `barcode_replacement_file`s: {barcode_replacement_files_links}.'
        )
        yield AuditFailure(audit_msg_unexpected_file.get('audit_category', ''), f'{detail} {audit_msg_unexpected_file.get("audit_description", "")}', level=audit_msg_unexpected_file.get('audit_level', ''))


def audit_pipeline_parameters(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets produced from uniform processing pipelines are expected to have pipeline parameters.",
            "audit_category": "missing pipeline parameters",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Documents or files linked as a pipeline parameter are expected to have document or content type of pipeline parameters.",
            "audit_category": "inconsistent pipeline parameters",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Documents with document type pipeline parameters are expected to be linked through the property pipeline parameters.",
            "audit_category": "inconsistent documents",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing_parameters = get_audit_message(audit_pipeline_parameters, index=0)
    audit_message_inconsistent_parameters = get_audit_message(audit_pipeline_parameters, index=1)
    audit_message_inconsistent_documents = get_audit_message(audit_pipeline_parameters, index=2)

    pipeline_parameters = value.get('pipeline_parameters', [])
    workflows = value.get('workflows', [])
    uniformly_processed = False
    for workflow in workflows:
        workflow_object = system.get('request').embed(workflow + '@@object?skip_calculated=true')
        if workflow_object['uniform_pipeline']:
            uniformly_processed = True
    if uniformly_processed and not (pipeline_parameters):
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has processed data from a uniform processing pipeline but no `pipeline_parameters`.'
        )
        yield AuditFailure(audit_message_missing_parameters.get('audit_category', ''), f'{detail} {audit_message_missing_parameters.get("audit_description", "")}', level=audit_message_missing_parameters.get('audit_level', ''))

    inconsistent_pipeline_parameters = []
    if pipeline_parameters:
        for pipeline_parameter in pipeline_parameters:
            pipeline_parameter_object = system.get('request').embed(
                pipeline_parameter + '@@object?skip_calculated=true')
            if pipeline_parameter.startswith('/documents/'):
                if pipeline_parameter_object['document_type'] != 'pipeline parameters':
                    inconsistent_pipeline_parameters.append(pipeline_parameter)
            else:
                if pipeline_parameter_object['content_type'] != 'pipeline parameters':
                    inconsistent_pipeline_parameters.append(pipeline_parameter)
    if inconsistent_pipeline_parameters:
        inconsistent_pipeline_parameters = ', '.join(
            [audit_link(path_to_text(pipeline_parameter), pipeline_parameter) for pipeline_parameter in inconsistent_pipeline_parameters])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `pipeline_parameters` with inconsistent `document_type` or `content_type`: {inconsistent_pipeline_parameters}.'
        )
        yield AuditFailure(audit_message_inconsistent_parameters.get('audit_category', ''), f'{detail} {audit_message_inconsistent_parameters.get("audit_description", "")}', level=audit_message_inconsistent_parameters.get('audit_level', ''))

    documents = value.get('documents', [])
    inconsistent_documents = []
    if documents:
        for document in documents:
            document_object = system.get('request').embed(document + '@@object?skip_calculated=true')
            if document_object['document_type'] == 'pipeline parameters':
                inconsistent_documents.append(document)
    if inconsistent_documents:
        inconsistent_documents = ', '.join(
            [audit_link(path_to_text(document), document) for document in inconsistent_documents])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has `documents`: {inconsistent_documents} with `document_type`: pipeline parameters.'
        )
        yield AuditFailure(audit_message_inconsistent_documents.get('audit_category', ''), f'{detail} {audit_message_inconsistent_documents.get("audit_description", "")}', level=audit_message_inconsistent_documents.get('audit_level', ''))


function_dispatcher_analysis_set_object = {
    'audit_analysis_set_multiplexed_samples': audit_analysis_set_multiplexed_samples,
    'audit_analysis_set_inconsistent_onlist_info': audit_analysis_set_inconsistent_onlist_info,
    'audit_missing_genome_transcriptome_references': audit_missing_genome_transcriptome_references,
    'audit_multiple_barcode_replacement_files_in_input': audit_multiple_barcode_replacement_files_in_input,
    'audit_pipeline_parameters': audit_pipeline_parameters
}


@audit_checker('AnalysisSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_analysis_set_object.values()))
def audit_analysis_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_analysis_set_object.keys():
        for failure in function_dispatcher_analysis_set_object[function_name](value, system):
            yield failure
