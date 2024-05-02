from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


@audit_checker('AnalysisSet', frame='object')
def audit_input_file_sets(value, system):
    '''
    [
        {
            "audit_description": "Primary analysis sets are expected to have at least one measurement set as an input file set.",
            "audit_category": "missing measurement set",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_input_file_sets)
    detail = ''
    if value.get('file_set_type') == 'primary analysis':
        if not(any(file_set.startswith('/measurement-sets/') for file_set in value['input_file_sets'])):
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'is a primary analysis, but does not specify any measurement sets in '
                f'`input_file_sets`.'
            )
            yield AuditFailure('missing measurement set', f'{detail} {description}', level='WARNING')


@audit_checker('AnalysisSet', frame='object')
def audit_input_file_sets_derived_from(value, system):
    '''
    [
        {
            "audit_description": "The file sets of the files that are used to derive the files in an analysis set are expected to be listed in the input file sets.",
            "audit_category": "missing input file set",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_input_file_sets_derived_from)
    detail = ''
    input_file_sets = value.get('input_file_sets', [])
    files = value.get('files', '')
    files_to_link = []
    derived_from_files_to_link = []
    missing_derived_from_file_sets = []
    if files:
        for file in files:
            file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
            derived_from_files = file_object.get('derived_from', '')
            if derived_from_files:
                for derived_from_file in derived_from_files:
                    derived_from_file_object = system.get('request').embed(
                        derived_from_file + '@@object?skip_calculated=true')
                    derived_from_file_set = derived_from_file_object['file_set']
                    if derived_from_file_set not in input_file_sets and derived_from_file_set != value['@id']:
                        files_to_link.append(file)
                        derived_from_files_to_link.append(derived_from_file)
                        missing_derived_from_file_sets.append(derived_from_file_set)
    if missing_derived_from_file_sets:
        files_to_link = ', '.join([audit_link(path_to_text(file), file) for file in files_to_link])
        derived_from_files_to_link = ', '.join([audit_link(path_to_text(file), file)
                                               for file in derived_from_files_to_link])
        missing_derived_from_file_sets = list(set(missing_derived_from_file_sets))
        missing_derived_from_file_sets = ', '.join(
            [audit_link(path_to_text(file_set), file_set) for file_set in missing_derived_from_file_sets])
        detail = (
            f'Analysis set {audit_link(path_to_text(value["@id"]),value["@id"])} '
            f'links to file(s) {files_to_link} that are `derived_from` '
            f'file(s) {derived_from_files_to_link} from file set(s) {missing_derived_from_file_sets} '
            f'which are not in `input_file_sets`.'
        )
        yield AuditFailure('missing input file set', f'{detail} {description}', level='ERROR')


@audit_checker('AnalysisSet', frame='object')
def audit_analysis_set_samples(value, system):
    '''
    [
        {
            "audit_description": "With the exception of multiplexed data, analysis sets are expected to specify all the samples from its input file sets.",
            "audit_category": "missing samples",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "With the exception of multiplexed data, analysis sets are expected to specify only the samples from its input file sets.",
            "audit_category": "unexpected samples",
            "audit_level": "WARNING"
        }
    ]
    '''
    missing_description = get_audit_description(audit_analysis_set_samples, index=0)
    unexpected_description = get_audit_description(audit_analysis_set_samples, index=1)
    detail = ''
    input_file_sets = value.get('input_file_sets')
    samples = value.get('samples')
    if input_file_sets:
        if samples:
            input_file_sets_samples = []
            for input_file_set in input_file_sets:
                input_file_set_object = system.get('request').embed(input_file_set + '@@object?skip_calculated=true')
                input_file_sets_samples.append(input_file_set_object.get('samples'))
            # flatten list
            input_file_sets_samples = [sample for sample_list in input_file_sets_samples for sample in sample_list]
            print(input_file_sets_samples)
            if not([input_file_sets_sample for input_file_sets_sample in input_file_sets_samples if input_file_sets_sample.startswith('/multiplexed-samples/')]):
                if set(samples).issubset(set(input_file_sets_samples)) and set(samples) != set(input_file_sets_samples):
                    missing_samples = list(set(input_file_sets_samples) - set(samples))
                    missing_samples = ', '.join([audit_link(path_to_text(missing_sample), missing_sample)
                                                for missing_sample in missing_samples])
                    detail = (
                        f'Analysis set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                        f'does not specify samples {missing_samples} from its `input_file_sets`. '
                    )
                    yield AuditFailure('missing samples', f'{detail} {missing_description}', level='WARNING')
                if (set(samples) - set(input_file_sets_samples)):
                    unexpected_samples = list(set(input_file_sets_samples) - set(samples))
                    unexpected_samples = ', '.join(
                        [audit_link(path_to_text(unexpected_sample), unexpected_sample) for unexpected_sample in unexpected_samples])
                    detail = (
                        f'Analysis set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                        f'specifies samples {unexpected_samples} not from its `input_file_sets`.'
                    )
                    yield AuditFailure('unexpected samples', f'{detail} {unexpected_description}', level='WARNING')
        else:
            detail = (
                f'Analysis set {audit_link(path_to_text(value["@id"]),value["@id"])} '
                f'has `input_file_sets`, but no `samples`.'
            )
            yield AuditFailure('missing samples', f'{detail} {missing_description}', level='WARNING')
