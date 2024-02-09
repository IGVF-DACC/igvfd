from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
)


def find_non_config_sequence_files(file_set):
    non_sequence_files = []
    for file in file_set.get('files'):
        if not(file.startswith('/sequence-files/') or file.startswith('/configuration-files/')):
            non_sequence_files.append(file)
    return non_sequence_files


@audit_checker('FileSet', frame='object')
def audit_no_files(value, system):
    '''
        audit_detail: File sets are expected to have files.
        audit_category: missing files
        audit_levels: WARNING
    '''
    if not(value.get('files', '')):
        detail = (
            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no files.'
        )
        yield AuditFailure('missing files', detail, level='WARNING')


@audit_checker('FileSet', frame='object')
def audit_missing_seqspec(value, system):
    '''
        audit_detail: Sequence files in a file set are expected to link to a seqspec file.
        audit_category: missing seqspec
        audit_levels: ERROR
    '''
    if 'files' in value:
        no_seqspec = []
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')
                if not sequence_file_object.get('seqspec'):
                    no_seqspec.append(file)
        if no_seqspec:
            no_seqspec = ', '.join([audit_link(path_to_text(file_no_seqspec), file_no_seqspec)
                                   for file_no_seqspec in no_seqspec])
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{no_seqspec} which do not have a seqspec configuration file.'
            )
            yield AuditFailure('missing seqspec', detail, level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_missing_seqspec_files(value, system):
    '''
        audit_detail: All files associated with a seqspec (both sequencing and seqspec files) are expected to be linked on the same file set.
        audit_category: missing related seqspec files
        audit_levels: ERROR
    '''
    if 'files' in value:
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')

                # Audit the file set with sequence files without the associated seqspec also in the file set.
                if sequence_file_object.get('seqspec'):
                    if sequence_file_object.get('seqspec') not in value['files']:
                        seqspec_path = sequence_file_object['seqspec']
                        detail = (
                            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file '
                            f'{audit_link(path_to_text(file), file)} which links to seqspec '
                            f'{audit_link(path_to_text(seqspec_path), seqspec_path)} which does not link to this file set.'
                        )
                        yield AuditFailure('missing related seqspec files', detail, level='ERROR')

            # Audit the file set with a seqspec configuration file without the associated sequence files also in the file set.
            if file.startswith('/configuration-files/'):
                configuration_file_object = system.get('request').embed(file)
                if configuration_file_object['content_type'] == 'seqspec' and configuration_file_object.get('seqspec_of'):
                    missing_sequence_files = list(set(configuration_file_object.get(
                        'seqspec_of', [])).difference(set(value['files'])))
                    if missing_sequence_files:
                        missing_sequence_files = ', '.join(
                            [audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in missing_sequence_files])
                        detail = (
                            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has seqspec configuration file '
                            f'{audit_link(path_to_text(file), file)} which links to sequence files: {missing_sequence_files} which '
                            f'do not link to this file set.'
                        )
                        yield AuditFailure('missing related seqspec files', detail, level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_inconsistent_seqspec(value, system):
    '''
        audit_detail: Sequence files in a file set from the same sequencing run and index are expected to link to the same seqspec file, which should be unique to that sequencing run and index.
        audit_category: inconsistent seqspec metadata
        audit_levels: ERROR
    '''
    if 'files' in value:
        sequence_file_to_seqspec = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')

                sequencing_run = str(sequence_file_object.get('sequencing_run', ''))
                flowcell_id = sequence_file_object.get('flowcell_id', '')
                lane = str(sequence_file_object.get('lane', ''))
                index = sequence_file_object.get('index', '')
                key_list = [sequencing_run, flowcell_id, lane, index]
                key_list = [item for item in key_list if item != '']
                key = ':'.join(key_list)

                if key not in sequence_file_to_seqspec:
                    sequence_file_to_seqspec[key] = {file: sequence_file_object.get('seqpsec', '')}
                else:
                    sequence_file_to_seqspec[key].update({file: sequence_file_object.get('seqpsec', '')})

        for key, file_dict in sequence_file_to_seqspec.items():
            first_seqspec = next(iter(file_dict.values()), None)
            if not(all(seqspec == first_seqspec for seqspec in file_dict.values())):
                non_matching_files = [file for file, seqspec in file_dict.items() if seqspec != first_seqspec]
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'{", ".join([audit_link(path_to_text(non_matching_files), non_matching_files) for non_matching_files in non_matching_files])} '
                    f'which belong to the same sequencing set, but do not share the same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

        seqspec_file_map = {}

        # Iterate through each key in sequence_file_to_seqspec
        for key, file_dict in sequence_file_to_seqspec.items():
            # Iterate through each file and its seqspec
            for file, seqspec in file_dict.items():
                # If the seqspec is not in the map, add it with the current file
                if seqspec not in seqspec_file_map:
                    seqspec_file_map[seqspec] = [(key, file)]
                else:
                    # If the seqspec is already in the map, add the current file
                    seqspec_file_map[seqspec].append((key, file))

        for seqspec, files in seqspec_file_map.items():
            if len(files) > 1:
                print(f'Error: Seqspec {seqspec} appears in the following files:')
                for key, file in files:
                    print(f'   File {file} under key {key}')
