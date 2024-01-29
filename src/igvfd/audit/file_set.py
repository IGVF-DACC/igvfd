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
            yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_missing_seqspec_files(value, system):
    '''
        audit_detail: All files associated with a seqspec (both sequencing and seqspec files) are expected to be linked on the same file set.
        audit_category: missing seqspec
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
                        yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

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
                        yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_inconsistent_seqspec(value, system):
    '''
        audit_detail: Sequence files in a file set from the same sequencing run are expected to link to the same seqspec file, which should be unique to that sequencing run.
        audit_category: inconsistent seqspec metadata
        audit_levels: ERROR
    '''
    if 'files' in value:
        sequencing_run_and_seqspecs = {}
        inconsistent_sequencing_runs = []
        shared_seqspec_sequencing_runs = []
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')

                # Get the mapping for sequencing_run to associated seqspec files.
                sequencing_run = str(sequence_file_object['sequencing_run'])
                if sequencing_run not in sequencing_run_and_seqspecs:
                    sequencing_run_and_seqspecs[sequencing_run] = [sequence_file_object.get('seqspec', '')]
                else:
                    sequencing_run_and_seqspecs[sequencing_run] += [sequence_file_object.get('seqspec', '')]

        for sequencing_run in sequencing_run_and_seqspecs:
            # if the associated seqspec files for a sequencing run are not all the same
            if len(set(sequencing_run_and_seqspecs[sequencing_run])) > 1:
                inconsistent_sequencing_runs.append(sequencing_run)

            seqspec_files = set(sequencing_run_and_seqspecs[sequencing_run])
            if sequencing_run in shared_seqspec_sequencing_runs:
                continue
            for other_sequencing_run, other_seqspecs in sequencing_run_and_seqspecs.items():
                if other_sequencing_run != sequencing_run:
                    if seqspec_files.intersection(other_seqspecs):
                        shared_seqspec_sequencing_runs.append(sequencing_run)

        # Audit the file set for the each sequencing run which links to multiple seqspec.
        if inconsistent_sequencing_runs:
            for sequencing_run in inconsistent_sequencing_runs:
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                    f'associated with sequencing runs {sequencing_run} which link to different '
                    f'seqspec files; sequence files from the same sequencing run are expected to link to the '
                    f'same seqspec file.'
                )
                yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')

        # Audit the file set with seperate sequencing runs which link to the same seqspec.
        if shared_seqspec_sequencing_runs:
            shared_seqspec_sequencing_runs = ', '.join(shared_seqspec_sequencing_runs)
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                f'associated with different sequencing runs {shared_seqspec_sequencing_runs} linking to the '
                f'same seqspec file; only sequence files from the same sequencing run are expected to link to the same seqspec file.'
            )
            yield AuditFailure('inconsistent seqspec metadata', detail, level='ERROR')
