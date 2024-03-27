from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_description
)


def find_non_config_sequence_files(file_set):
    non_sequence_files = []
    for file in file_set.get('files'):
        if not(file.startswith('/sequence-files/') or file.startswith('/configuration-files/')):
            non_sequence_files.append(file)
    return non_sequence_files


def load_chrom_sizes_file(file_path):
    chromosome_sizes = {}
    with open(file_path, 'r') as file:
        for line in file:
            lines = line.split('\t')
            chromosome = lines[0]
            size = int(lines[1])
            chromosome_sizes[chromosome] = size
    return chromosome_sizes


@audit_checker('FileSet', frame='object')
def audit_no_files(value, system):
    '''
    [
        {
            "audit_description": "File sets are expected to have files.",
            "audit_category": "missing files",
            "audit_level": "WARNING"
        }
    ]
    '''
    description = get_audit_description(audit_no_files)
    if not(value.get('files', '')):
        detail = (
            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `files`.'
        )
        yield AuditFailure('missing files', f'{detail} {description}', level='WARNING')


@audit_checker('FileSet', frame='object')
def audit_missing_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Sequence files in a file set are expected to link to a sequence specification file.",
            "audit_category": "missing sequence specification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    description = get_audit_description(audit_missing_seqspec)
    if 'files' in value:
        no_seqspec = []
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)
                if not sequence_file_object.get('seqspecs'):
                    no_seqspec.append(file)
        if no_seqspec:
            no_seqspec = ', '.join([audit_link(path_to_text(file_no_seqspec), file_no_seqspec)
                                   for file_no_seqspec in no_seqspec])
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{no_seqspec} which do not have any `seqspecs`.'
            )
            yield AuditFailure('missing sequence specification', f'{detail} {description}', level='NOT_COMPLIANT')


@audit_checker('FileSet', frame='object')
def audit_files_associated_with_incorrect_fileset(value, system):
    '''
    [
        {
            "audit_description": "All files associated with a seqspec (both sequencing and seqspec files) are expected to be linked to the same file set.",
            "audit_category": "missing related files",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_files_associated_with_incorrect_fileset)
    if 'files' in value:
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)

                # Audit the file set with sequence files without the associated seqspec also in the file set.
                if sequence_file_object.get('seqspecs'):
                    for configuration_file in sequence_file_object.get('seqspecs'):
                        if configuration_file not in value['files']:
                            detail = (
                                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file '
                                f'{audit_link(path_to_text(file), file)} which links to seqspec '
                                f'{audit_link(path_to_text(configuration_file), configuration_file)} which does not link to this file set.'
                            )
                            yield AuditFailure('missing related files', f'{detail} {description}', level='ERROR')

            # Audit the file set with a seqspec configuration file without the associated sequence files also in the file set.
            if file.startswith('/configuration-files/'):
                configuration_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')
                if configuration_file_object['content_type'] == 'seqspec' and configuration_file_object.get('seqspec_of'):
                    missing_sequence_files = list(set(configuration_file_object.get(
                        'seqspec_of', [])).difference(set(value['files'])))
                    if missing_sequence_files:
                        missing_sequence_files = ', '.join(
                            [audit_link(path_to_text(sequence_file), sequence_file) for sequence_file in missing_sequence_files])
                        detail = (
                            f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has seqspec configuration file '
                            f'{audit_link(path_to_text(file), file)} which links to sequence file(s): {missing_sequence_files} which '
                            f'do not link to this file set.'
                        )
                        yield AuditFailure('missing related files', f'{detail} {description}', level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_inconsistent_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Sequence files in a file set from the same sequencing run, flowcell_id, lane, and index are expected to link to the same seqspec file, which should be unique to that set of sequence files.",
            "audit_category": "inconsistent sequence specifications",
            "audit_level": "ERROR"
        }
    ]
    '''
    description = get_audit_description(audit_inconsistent_seqspec)
    if 'files' in value:
        sequence_to_seqspec = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)

                sequencing_run = str(sequence_file_object.get('sequencing_run'))
                flowcell_id = sequence_file_object.get('flowcell_id', '')
                lane = str(sequence_file_object.get('lane', ''))
                index = sequence_file_object.get('index', '')
                key_list = [sequencing_run, flowcell_id, lane, index]
                key_list = [item for item in key_list if item != '']
                key = ':'.join(key_list)

                if key not in sequence_to_seqspec:
                    sequence_to_seqspec[key] = {file: set(sequence_file_object.get('seqspecs', []))}
                else:
                    sequence_to_seqspec[key][file] = set(sequence_file_object.get('seqspecs', []))

        for key, file_dict in sequence_to_seqspec.items():
            first_seqspec = next(iter(file_dict.values()), None)
            if not(all(seqspec == first_seqspec for seqspec in file_dict.values())):
                non_matching_files = [file for file, _ in file_dict.items()]
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files: '
                    f'{", ".join([audit_link(path_to_text(non_matching_files), non_matching_files) for non_matching_files in non_matching_files])} '
                    f'which belong to the same sequencing set, but do not have the same `seqspecs`.'
                )
                yield AuditFailure('inconsistent sequence specifications', f'{detail} {description}', level='ERROR')

        seqspec_to_sequence = {}
        for key, file_dict in sequence_to_seqspec.items():
            for file, seqspec in file_dict.items():
                if seqspec:
                    seqspec_str_formatted = ':'.join(sorted(list(seqspec)))
                    if seqspec_str_formatted not in seqspec_to_sequence:
                        seqspec_to_sequence[seqspec_str_formatted] = [(key, file)]
                    else:
                        seqspec_to_sequence[seqspec_str_formatted].append((key, file))

        for seqspec, sequence_files in seqspec_to_sequence.items():
            key_set = set()
            for key, file in sequence_files:
                key_set.add(key)
            if len(key_set) > 1:
                seqspec_paths = [audit_link(path_to_text(x), x) for x in seqspec.split(':')]
                detail = (
                    f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files: '
                    f'{", ".join([audit_link(path_to_text(file), file) for _, file in sequence_files])} '
                    f'which share the same `seqspecs` {", ".join(seqspec_paths)} '
                    f'but belong to different sequencing sets.'
                )
                yield AuditFailure('inconsistent sequence specifications', f'{detail} {description}', level='ERROR')


@audit_checker('FileSet', frame='object')
def audit_loci_valid_chrom_sizes(value, system):
    '''
    [
        {
            "audit_description": "Loci are expected to belong to the same assembly.",
            "audit_category": "inconsistent loci",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Loci are expected to specify a valid chromosome name and range from its respective assembly.",
            "audit_category": "inconsistent loci",
            "audit_level": "ERROR"
        }
    ]
    '''
    description_inconsistent_assembly = get_audit_description(audit_loci_valid_chrom_sizes, 0)
    description_inconsistent_loci = get_audit_description(audit_loci_valid_chrom_sizes, 1)
    GRCh38_chrom_sizes = load_chrom_sizes_file('src/igvfd/audit/_static/GRCh38.chrom.sizes')
    GRCm39_chrom_sizes = load_chrom_sizes_file('src/igvfd/audit/_static/mm39.chrom.sizes')
    invalid_chroms = []
    invalid_loci = []
    if 'small_scale_loci_list' in value:
        if len(set([loci['assembly'] for loci in value['small_scale_loci_list']])) > 1:
            assemblies = ', '.join(set(loci['assembly'] for loci in value['small_scale_loci_list']))
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has loci '
                f'from multiple assemblies: {assemblies} listed in its `small_scale_loci_list`.'
            )
            yield AuditFailure('inconsistent loci', f'{detail} {description_inconsistent_assembly}', level='ERROR')
        for loci in value['small_scale_loci_list']:
            if loci['assembly'] == 'GRCh38':
                if loci['chromosome'] not in GRCh38_chrom_sizes:
                    invalid_chroms.append(loci['chromosome'])
                elif loci['start'] > GRCh38_chrom_sizes[loci['chromosome']] or loci['end'] > GRCh38_chrom_sizes[loci['chromosome']]:
                    invalid_loci.append(loci)
            elif loci['assembly'] == 'GRCm39':
                if loci['chromosome'] not in GRCm39_chrom_sizes:
                    invalid_chroms.append(loci['chromosome'])
                elif loci['start'] > GRCm39_chrom_sizes[loci['chromosome']] or loci['end'] > GRCm39_chrom_sizes[loci['chromosome']]:
                    invalid_loci.append(loci)
        if invalid_chroms:
            invalid_chroms = ', '.join(invalid_chroms)
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has unexpected '
                f'chromosome(s): {invalid_chroms} listed in its `small_scale_loci_list`.'
            )
            yield AuditFailure('inconsistent loci', f'{detail} {description_inconsistent_loci}', level='ERROR')
        if invalid_loci:
            invalid_loci = ', '.join(str(invalid_locus) for invalid_locus in invalid_loci)
            detail = (
                f'File set {audit_link(path_to_text(value["@id"]), value["@id"])} has loci '
                f'listed in `small_scale_loci_list`: {invalid_loci} which exceed '
                f'the valid chromosome size for its respective chromosome.'
            )
            yield AuditFailure('inconsistent loci', f'{detail} {description_inconsistent_loci}', level='ERROR')
