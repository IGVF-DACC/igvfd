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
        sequencing_runs = {}
        indices = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')

                # Get the mapping for index and sequencing_runs to sequence files and associated seqspec. A sequence file will only be audited wrt index or sequencing run.
                if 'index' in sequence_file_object:
                    index = str(sequence_file_object['index'])
                    if index in indices:
                        indices[index][file] = {'seqspec': sequence_file_object.get('seqspec', '')}
                    else:
                        indices[index] = {file: {'seqspec': sequence_file_object.get('seqspec', '')}}
                else:
                    sequencing_run = str(sequence_file_object['sequencing_run'])
                    if sequencing_run in sequencing_runs:
                        sequencing_runs[sequencing_run][file] = {'seqspec': sequence_file_object.get('seqspec', '')}
                    else:
                        sequencing_runs[sequencing_run] = {file: {'seqspec': sequence_file_object.get('seqspec', '')}}

        # Check that associated seqspec files for an index are the same
        for index, sequence_files in indices.items():
            unique_seqspecs = set(file_data['seqspec'] for file_data in sequence_files.values() if file_data['seqspec'])
            if len(unique_seqspecs) != 1:
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'{", ".join([audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in indices[index].keys()])} '
                    f'associated with index {index} which do not link to the same seqspec file; '
                    f'sequence files with the same index are expected to link to the '
                    f'same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

        # Check that associated seqspec files for a sequencing run are the same
        for sequencing_run, sequence_files in sequencing_runs.items():
            unique_seqspecs = set(file_data['seqspec'] for file_data in sequence_files.values() if file_data['seqspec'])
            if len(unique_seqspecs) != 1:
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'{", ".join([audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in sequencing_runs[sequencing_run].keys()])} '
                    f'associated with sequencing run {sequencing_run} do not link to the same seqspec file; '
                    f'sequence files from the same sequencing run are expected to link to the '
                    f'same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

        # Check that associated seqspec files are unique for each index
        for index, sequence_files in indices.items():
            share_seqspec = []
            seqspec = set(file_data['seqspec'] for file_data in sequence_files.values() if file_data['seqspec'])
            for index_to_compare, sequence_files_to_compare in indices.items():
                if index == index_to_compare:
                    continue
                else:
                    if seqspec.intersection(set(file_data['seqspec'] for file_data in sequence_files_to_compare.values())):
                        share_seqspec.append(index_to_compare)
            if share_seqspec:
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'{", ".join([audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in indices[index].keys()])} '
                    f'with index {index} sharing the same seqspec file as files associated with index(es) {", ".join(share_seqspec)}; '
                    f'only sequence files with the same index are expected to link to the same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

        # Check that associated seqspec files are unique for each sequencing run
        for sequencing_run, sequence_files in sequencing_runs.items():
            share_seqspec = []
            seqspec = set(file_data['seqspec'] for file_data in sequence_files.values() if file_data['seqspec'])
            for sequencing_run_to_compare, sequence_files_to_compare in sequencing_runs.items():
                if sequencing_run == sequencing_run_to_compare:
                    continue
                else:
                    if seqspec.intersection(set(file_data['seqspec'] for file_data in sequence_files_to_compare.values())):
                        share_seqspec.append(sequencing_run_to_compare)
            if share_seqspec:
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'{", ".join([audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in sequencing_runs[sequencing_run].keys()])} '
                    f'from sequencing run {sequencing_run} sharing the same seqspec file as files associated with sequencing run(s) {", ".join(share_seqspec)}; '
                    f'only sequence files with the same sequencing run are expected to link to the same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')
