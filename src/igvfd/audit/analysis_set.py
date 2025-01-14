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
            "audit_level": "NOT_COMPLIANT"
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
        files_to_link = ', '.join([audit_link(path_to_text(file), file) for file in set(files_to_link)])
        derived_from_files_to_link = ', '.join([audit_link(path_to_text(file), file)
                                               for file in set(derived_from_files_to_link)])
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
def audit_analysis_set_files_missing_analysis_step_version(value, system):
    '''
    [
        {
            "audit_description": "Analysis set files are expected to specify analysis step version.",
            "audit_category": "missing analysis step version",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message_missing_step_version = get_audit_message(
        audit_analysis_set_files_missing_analysis_step_version, index=0)
    files = value.get('files')
    files_with_missing_asv = []
    for file in files:
        file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
        if file_object.get('derived_manually', ''):
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


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_multiple_workflows(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets are not expected to link to more than one workflow.",
            "audit_category": "unexpected workflows",
            "audit_level": "WARNING"
        }
    ]
    '''
    audit_message_multiple_workflows = get_audit_message(audit_analysis_set_multiple_workflows, index=0)
    workflows = value.get('workflows', [])
    if len(workflows) > 1:
        file_workflow_report = []
        files = value.get('files')
        for file in files:
            file_object = system.get('request').embed(file + '@@object?skip_caluculated=true')
            file_analysis_step_version = file_object.get('analysis_step_version', '')
            if file_analysis_step_version:
                file_analysis_step_version_obj = system.get('request').embed(
                    file_analysis_step_version + '@@object?skip_caluculated=true')
                file_analysis_step = file_analysis_step_version_obj.get('analysis_step', '')
                if file_analysis_step:
                    file_analysis_step_obj = system.get('request').embed(
                        file_analysis_step + '@@object?skip_caluculated=true')
                    file_workflow = file_analysis_step_obj.get('workflow', '')
                if file_workflow:
                    excess_workflows_report = ' has '.join(
                        [audit_link(path_to_text(file), file), audit_link(path_to_text(file_workflow), file_workflow)])
                    file_workflow_report.append(excess_workflows_report)
        details = (
            f'Analysis set {audit_link(path_to_text(value["@id"]), value["@id"])} has multiple '
            f'`workflows` with {", ".join(file_workflow_report)}.'
        )
        yield AuditFailure(audit_message_multiple_workflows.get('audit_category', ''),
                           f'{details} {audit_message_multiple_workflows.get("audit_description", "")}',
                           audit_message_multiple_workflows.get('audit_level', '')
                           )


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_multiplexed_samples(value, system):
    '''
    [
        {
            "audit_description": "Analysis sets with multiplexed samples are expected to specify a demultiplexed sample.",
            "audit_category": "missing demultiplexed sample",
            "audit_level": "WARNING"
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
