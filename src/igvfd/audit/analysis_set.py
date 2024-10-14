from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message
)


@audit_checker('AnalysisSet', frame='object')
def audit_input_file_sets_derived_from(value, system):
    '''
    [
        {
            "audit_description": "The file sets of the files that are used to derive the files in an analysis set are expected to be listed in the input file sets.",
            "audit_category": "missing input file set",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Files in an analysis set are expected to be derived from other files.",
            "audit_category": "missing derived from",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "The analysis set input files are expected to belong to the input file sets.",
            "audit_category": "unexpected input file set",
            "audit_level": "ERROR"
        }
    ]
    '''
    audit_message_missing_input_file_set = get_audit_message(audit_input_file_sets_derived_from, index=0)
    audit_message_missing_derived_from = get_audit_message(audit_input_file_sets_derived_from, index=1)
    audit_message_unexpected_input_file_set = get_audit_message(audit_input_file_sets_derived_from, index=2)
    detail = ''
    input_file_sets = value.get('input_file_sets', [])
    files = value.get('files', '')
    files_to_link = []
    derived_from_files_to_link = []
    missing_derived_from_file_sets = []
    missing_derived_from = []
    all_derived_from_file_sets = []
    if files:
        for file in files:
            file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
            derived_from_files = file_object.get('derived_from', '')
            if derived_from_files:
                for derived_from_file in derived_from_files:
                    derived_from_file_object = system.get('request').embed(
                        derived_from_file + '@@object?skip_calculated=true')
                    derived_from_file_set = derived_from_file_object['file_set']
                    all_derived_from_file_sets.append(derived_from_file_set)
                    if derived_from_file_set not in input_file_sets and derived_from_file_set != value['@id']:
                        files_to_link.append(file)
                        derived_from_files_to_link.append(derived_from_file)
                        missing_derived_from_file_sets.append(derived_from_file_set)
            else:
                missing_derived_from.append(file)
    if missing_derived_from_file_sets:
        files_to_link = ', '.join([audit_link(path_to_text(file), file) for file in files_to_link])
        derived_from_files_to_link = ', '.join([audit_link(path_to_text(file), file)
                                               for file in derived_from_files_to_link])
        missing_derived_from_file_sets = list(set(missing_derived_from_file_sets))
        missing_derived_from_file_sets = ', '.join(
            [audit_link(path_to_text(file_set), file_set) for file_set in missing_derived_from_file_sets])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {files_to_link} that are `derived_from` '
            f'file(s) {derived_from_files_to_link} from file set(s) {missing_derived_from_file_sets} '
            f'which are not in `input_file_sets`.'
        )
        yield AuditFailure(audit_message_missing_input_file_set.get('audit_category', ''), f'{detail} {audit_message_missing_input_file_set.get("audit_description", "")}', level=audit_message_missing_input_file_set.get('audit_level', ''))
    if missing_derived_from:
        missing_derived_from = ', '.join([audit_link(path_to_text(file), file) for file in missing_derived_from])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {missing_derived_from} that have no `derived_from`.'
        )
        yield AuditFailure(audit_message_missing_derived_from.get('audit_category', ''), f'{detail} {audit_message_missing_derived_from.get("audit_description", "")}', level=audit_message_missing_derived_from.get('audit_level', ''))
    unexpected_file_sets = list(set(input_file_sets) - set(all_derived_from_file_sets))
    if unexpected_file_sets:
        unexpected_file_sets = ', '.join(
            [audit_link(path_to_text(file_set), file_set) for file_set in unexpected_file_sets])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file set(s): {unexpected_file_sets} in `input_file_sets` that are not represented in the '
            f'`derived_from` of the file sets of the files in this analysis.'
        )
        yield AuditFailure(audit_message_unexpected_input_file_set.get('audit_category', ''), f'{detail} {audit_message_unexpected_input_file_set.get("audit_description", "")}', level=audit_message_unexpected_input_file_set.get('audit_level', ''))


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_samples(value, system):
    '''
    [
        {
            "audit_description": "With the exception of multiplexed data, analysis sets are expected to specify all the samples associated with its input file sets.",
            "audit_category": "missing samples",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "With the exception of multiplexed data, analysis sets are expected to specify only the samples associated with its input file sets.",
            "audit_category": "unexpected samples",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message_missing_samples = get_audit_message(audit_analysis_set_samples, index=0)
    audit_message_unexpected_samples = get_audit_message(audit_analysis_set_samples, index=1)
    detail = ''
    input_file_sets = value.get('input_file_sets')
    samples = value.get('samples')
    if input_file_sets:
        if samples:
            input_file_sets_samples = []
            for input_file_set in input_file_sets:
                input_file_set_object = system.get('request').embed(input_file_set + '@@object?skip_calculated=true')
                input_file_set_samples = input_file_set_object.get('samples')
                if input_file_set_samples:
                    input_file_sets_samples.append(input_file_set_samples)
            # flatten list
            input_file_sets_samples = [sample for sample_list in input_file_sets_samples for sample in sample_list]
            if not ([input_file_sets_sample for input_file_sets_sample in input_file_sets_samples if input_file_sets_sample.startswith('/multiplexed-samples/')]):
                if set(samples).issubset(set(input_file_sets_samples)) and set(samples) != set(input_file_sets_samples):
                    missing_samples = list(set(input_file_sets_samples) - set(samples))
                    missing_samples = ', '.join([audit_link(path_to_text(missing_sample), missing_sample)
                                                for missing_sample in missing_samples])
                    detail = (
                        f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'does not specify samples {missing_samples} associated with its `input_file_sets`. '
                    )
                    yield AuditFailure(audit_message_missing_samples.get('audit_category', ''), f'{detail} {audit_message_missing_samples.get("audit_description", "")}', level=audit_message_missing_samples.get('audit_level', ''))
                unexpected_samples = list(set(samples) - set(input_file_sets_samples))
                if unexpected_samples:
                    unexpected_samples = ', '.join(
                        [audit_link(path_to_text(unexpected_sample), unexpected_sample) for unexpected_sample in unexpected_samples])
                    detail = (
                        f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                        f'specifies samples {unexpected_samples} not associated with its `input_file_sets`.'
                    )
                    yield AuditFailure(audit_message_unexpected_samples.get('audit_category', ''), f'{detail} {audit_message_unexpected_samples.get("audit_description", "")}', level=audit_message_unexpected_samples.get('audit_level', ''))
        else:
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
                f'has `input_file_sets`, but no `samples`.'
            )
            yield AuditFailure(audit_message_missing_samples.get('audit_category', ''), f'{detail} {audit_message_missing_samples.get("audit_description", "")}', level=audit_message_missing_samples.get('audit_level', ''))


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_files_missing_analysis_step_version(value, system):
    '''
    [
        {
            "audit_description": "Analysis set files are expected to specify analysis step version.",
            "audit_category": "missing analysis step version",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message_missing_step_version = get_audit_message(
        audit_analysis_set_files_missing_analysis_step_version, index=0)
    files = value.get('files')
    files_with_missing_asv = []
    for file in files:
        file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
        if file_object.get('derived_manually') is True:
            continue
        if not (file_object.get('analysis_step_version', '')):
            files_with_missing_asv.append(file)
    if files_with_missing_asv:
        files_with_missing_asv = ', '.join([audit_link(path_to_text(file), file) for file in files_with_missing_asv])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {files_with_missing_asv} that are missing `analysis_step_version`.'
        )
        yield AuditFailure(audit_message_missing_step_version.get('audit_category', ''), f'{detail} {audit_message_missing_step_version.get("audit_description", "")}', level=audit_message_missing_step_version.get('audit_level', ''))
