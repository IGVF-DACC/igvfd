from snovault.auditor import (
    audit_checker,
    AuditFailure,
)
from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words
)


SINGLE_CELL_ASSAY_TERMS = ['/assay-terms/OBI_0002762/',  # single-nucleus ATAC-seq
                           '/assay-terms/OBI_0003109/',  # single-nucleus RNA sequencing assay
                           '/assay-terms/OBI_0002631/',  # single-cell RNA sequencing assay
                           '/assay-terms/OBI_0002764/',  # single-cell ATAC-seq
                           '/assay-terms/OBI_0003660/'  # in vitro CRISPR screen using single-cell RNA-seq
                           ]


def load_chrom_sizes_file(file_path):
    chromosome_sizes = {}
    with open(file_path, 'r') as file:
        for line in file:
            lines = line.split('\t')
            chromosome = lines[0]
            size = int(lines[1])
            chromosome_sizes[chromosome] = size
    return chromosome_sizes


def single_cell_check(system, value, object_type, single_cell_assay_terms=SINGLE_CELL_ASSAY_TERMS):
    if object_type == 'Measurement set':
        assay_term = value.get('assay_term')
        return assay_term in single_cell_assay_terms
    elif object_type == 'Auxiliary set':
        measurement_sets = value.get('measurement_sets')
        for measurement_set in measurement_sets:
            measurement_set_obj = system.get('request').embed(measurement_set, '@@object?skip_calculated=true')
            assay_term = measurement_set_obj.get('assay_term')
            if assay_term in single_cell_assay_terms:
                return True
        return False
    elif object_type == 'Construct library set':
        samples = value.get('applied_to_samples')
        for sample in samples:
            sample_obj = system.get('request').embed(
                sample, '@@object_with_select_calculated_properties?field=file_sets')
            file_sets = sample_obj.get('file_sets')
            for file_set in file_sets:
                if file_set.startswith('/measurement-sets/'):
                    measurement_set_obj = system.get('request').embed(file_set, '@@object?skip_calculated=true')
                    assay_term = measurement_set_obj.get('assay_term')
                    if assay_term in single_cell_assay_terms:
                        return True
        return False
    elif object_type == 'Analysis set':
        for input_file_set in value.get('input_file_sets', []):
            if input_file_set.startswith('/measurement-sets/'):
                measurement_set_obj = system.get('request').embed(input_file_set, '@@object?skip_calculated=true')
                assay_term = measurement_set_obj.get('assay_term')
                if assay_term in single_cell_assay_terms:
                    return True
        return False
    else:
        return False


@audit_checker('FileSet', frame='object')
def audit_no_files(value, system):
    '''
    [
        {
            "audit_description": "File sets are expected to have files.",
            "audit_category": "missing files",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_missing_files = get_audit_message(audit_no_files, index=0)
    if not (value.get('files', '')) and object_type != 'Construct library set':
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `files`.'
        )
        yield AuditFailure(audit_message_missing_files.get('audit_category', ''), f'{detail} {audit_message_missing_files.get("audit_description", "")}', level=audit_message_missing_files.get('audit_level', ''))


@audit_checker('FileSet', frame='object')
def audit_missing_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Sequence files in a file set associated with bulk data are expected to link to a sequence specification file.",
            "audit_category": "missing sequence specification",
            "audit_level": "INTERNAL_ACTION"
        },
        {
            "audit_description": "Sequence files in a file set associated with single cell data are expected to link to a sequence specification file.",
            "audit_category": "missing sequence specification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
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
            if single_cell_check(system, value, object_type):
                audit_message = get_audit_message(audit_missing_seqspec, index=1)
            else:
                audit_message = get_audit_message(audit_missing_seqspec, index=0)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{no_seqspec} which do not have any `seqspecs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_files_associated_with_incorrect_fileset)
    if 'files' in value:
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)

                # Audit the file set with sequence files without the associated seqspec also in the file set.
                if sequence_file_object.get('seqspecs'):
                    for configuration_file in sequence_file_object.get('seqspecs'):
                        if configuration_file not in value['files']:
                            detail = (
                                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file '
                                f'{audit_link(path_to_text(file), file)} which links to seqspec '
                                f'{audit_link(path_to_text(configuration_file), configuration_file)} which does not link to this file set.'
                            )
                            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))

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
                            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has seqspec configuration file '
                            f'{audit_link(path_to_text(file), file)} which links to sequence file(s): {missing_sequence_files} which '
                            f'do not link to this file set.'
                        )
                        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('FileSet', frame='object')
def audit_inconsistent_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Sequence files in a file set from the same sequencing set are expected to link to the same seqspec file, which should be unique to that sequencing set. A sequencing set is defined by the combination of flowcell ID, lane, and index for non-single cell data, or flowcell ID, lane, index, and sequencing run for single cell data.",
            "audit_category": "inconsistent sequence specifications",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_inconsistent_seqspec)
    if 'files' in value:
        sequence_to_seqspec = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)

                sequencing_run = str(sequence_file_object.get('sequencing_run'))
                flowcell_id = sequence_file_object.get('flowcell_id', '')
                lane = str(sequence_file_object.get('lane', ''))
                index = sequence_file_object.get('index', '')
                if single_cell_check(system, value, object_type):
                    key_list = [sequencing_run, flowcell_id, lane, index]
                else:
                    key_list = [flowcell_id, lane, index]
                key_list = [item for item in key_list if item != '']
                key = ':'.join(key_list)

                if key not in sequence_to_seqspec:
                    sequence_to_seqspec[key] = {file: set(sequence_file_object.get('seqspecs', []))}
                else:
                    sequence_to_seqspec[key][file] = set(sequence_file_object.get('seqspecs', []))

        for key, file_dict in sequence_to_seqspec.items():
            first_seqspec = next(iter(file_dict.values()), None)
            if not (all(seqspec == first_seqspec for seqspec in file_dict.values())):
                non_matching_files = [file for file, _ in file_dict.items()]
                detail = (
                    f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files: '
                    f'{", ".join([audit_link(path_to_text(non_matching_files), non_matching_files) for non_matching_files in non_matching_files])} '
                    f'which belong to the same sequencing set, but do not have the same `seqspecs`.'
                )
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))

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
                    f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files: '
                    f'{", ".join([audit_link(path_to_text(file), file) for _, file in sequence_files])} '
                    f'which share the same `seqspecs` {", ".join(seqspec_paths)}, '
                    f'but belong to different sequencing sets.'
                )
                yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('ConstructLibrarySet', frame='object')
@audit_checker('PredictionSet', frame='object')
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
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_inconsistent_assembly = get_audit_message(audit_loci_valid_chrom_sizes, index=0)
    audit_message_inconsistent_loci = get_audit_message(audit_loci_valid_chrom_sizes, index=1)
    GRCh38_chrom_sizes = load_chrom_sizes_file('src/igvfd/audit/_static/GRCh38.chrom.sizes')
    GRCm39_chrom_sizes = load_chrom_sizes_file('src/igvfd/audit/_static/GRCm39.chrom.sizes')
    chrom_sizes = {'GRCh38': GRCh38_chrom_sizes, 'GRCm39': GRCm39_chrom_sizes}
    invalid_chroms = []
    invalid_loci = []
    if 'small_scale_loci_list' in value:
        if len(set([loci['assembly'] for loci in value['small_scale_loci_list']])) > 1:
            assemblies = ', '.join(set(loci['assembly'] for loci in value['small_scale_loci_list']))
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has loci '
                f'from multiple assemblies: {assemblies} listed in its `small_scale_loci_list`.'
            )
            yield AuditFailure(audit_message_inconsistent_assembly.get('audit_category', ''), f'{detail} {audit_message_inconsistent_assembly.get("audit_description", "")}', level=audit_message_inconsistent_assembly.get('audit_level', ''))
        for loci in value['small_scale_loci_list']:
            assembly = chrom_sizes[loci['assembly']]
            if loci['chromosome'] not in assembly:
                invalid_chroms.append(loci['chromosome'])
            elif loci['start'] > assembly[loci['chromosome']] or loci['end'] > assembly[loci['chromosome']]:
                invalid_loci.append(loci)
        if invalid_chroms:
            invalid_chroms = ', '.join(invalid_chroms)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has unexpected '
                f'chromosome(s): {invalid_chroms} listed in its `small_scale_loci_list`.'
            )
            yield AuditFailure(audit_message_inconsistent_loci.get('audit_category', ''), f'{detail} {audit_message_inconsistent_loci.get("audit_description", "")}', level=audit_message_inconsistent_loci.get('audit_level', ''))
        if invalid_loci:
            invalid_loci = ', '.join(str(invalid_locus) for invalid_locus in invalid_loci)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has loci '
                f'listed in `small_scale_loci_list`: {invalid_loci} which exceed '
                f'the valid chromosome size for its respective chromosome.'
            )
            yield AuditFailure(audit_message_inconsistent_loci.get('audit_category', ''), f'{detail} {audit_message_inconsistent_loci.get("audit_description", "")}', level=audit_message_inconsistent_loci.get('audit_level', ''))


@audit_checker('FileSet', frame='object')
def audit_inconsistent_sequencing_kit(value, system):
    '''
    [
        {
            "audit_description": "Sequence files should specify a sequencing kit which is consistent with their sequencing platform. Sequence files in the same sequencing run should also specify the same sequencing kit.",
            "audit_category": "inconsistent sequencing kit",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Sequence files in a file set associated wtih bulk data should specify a sequencing kit.",
            "audit_category": "missing sequencing kit",
            "audit_level": "INTERNAL_ACTION"
        },
        {
            "audit_description": "Sequence files in a file set associated wtih single cell data should specify a sequencing kit.",
            "audit_category": "missing sequencing kit",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_inconsistent_kit = get_audit_message(audit_inconsistent_sequencing_kit, index=0)
    if 'files' in value:
        file_info = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)

                sequencing_run = str(sequence_file_object.get('sequencing_run'))
                sequencing_kit = sequence_file_object.get('sequencing_kit', '')
                sequencing_platform = sequence_file_object.get('sequencing_platform', '').get('@id')

                file_info[file] = {'kit': sequencing_kit, 'run': sequencing_run, 'platform': sequencing_platform}
    if not file_info:
        return

    missing_kit = []
    for file in file_info:
        if file_info[file]['kit'] == '':
            missing_kit.append(file)
        else:
            if file_info[file]['platform'] != '':
                platform_object = system.get('request').embed(file_info[file]['platform'])
                if file_info[file]['kit'] not in platform_object.get('sequencing_kits', []):
                    detail = (
                        f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has a sequence '
                        f'file {audit_link(path_to_text(file), file)} sequenced on a `sequencing_platform` '
                        f'{audit_link(path_to_text(file_info[file]["platform"]), file_info[file]["platform"])} '
                        f'that is inconsistent with its `sequencing_kit` {file_info[file]["kit"]}.'
                    )
                    yield AuditFailure(audit_message_inconsistent_kit.get('audit_category', ''), f'{detail} {audit_message_inconsistent_kit.get("audit_description", "")}', level=audit_message_inconsistent_kit.get('audit_level', ''))

    if missing_kit:
        if single_cell_check(system, value, object_type):
            audit_message_missing_kit = get_audit_message(audit_inconsistent_sequencing_kit, index=2)
        else:
            audit_message_missing_kit = get_audit_message(audit_inconsistent_sequencing_kit, index=1)
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence '
            f'file(s) {", ".join([audit_link(path_to_text(f), f) for f in missing_kit])} '
            f'which lack specification of a `sequencing_kit`.'
        )
        yield AuditFailure(audit_message_missing_kit.get('audit_category', ''), f'{detail} {audit_message_missing_kit.get("audit_description", "")}', level=audit_message_missing_kit.get('audit_level', ''))

    run_to_kit = {}
    for file in file_info:
        if file_info[file]['run'] in run_to_kit:
            run_to_kit[file_info[file]['run']]['files'].append(file)
            run_to_kit[file_info[file]['run']]['kits'].append(file_info[file]['kit'])
        else:
            run_to_kit[file_info[file]['run']] = {
                'files': [file],
                'kits': [file_info[file]['kit']]
            }

    for run in run_to_kit:
        if len(set(run_to_kit[run]['kits'])) > 1:
            unspecified_kit_phrase = ''
            if None in run_to_kit[run]['kits'] or '' in run_to_kit[run]['kits']:
                unspecified_kit_phrase = ' and unspecified kit(s)'
            filtered_kits = [kit for kit in run_to_kit[run]['kits'] if kit not in [None, '']]
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence files '
                f'{", ".join([audit_link(path_to_text(f), f) for f in run_to_kit[run]["files"]])} '
                f'which are part of the same sequencing run, but do not specify the same `sequencing_kit`: '
                f'{", ".join(filtered_kits)}{unspecified_kit_phrase}.'
            )
            yield AuditFailure(audit_message_inconsistent_kit.get('audit_category', ''), f'{detail} {audit_message_inconsistent_kit.get("audit_category", "")}', level=audit_message_inconsistent_kit.get('audit_level', ''))


@audit_checker('AuxiliarySet', frame='object')
@audit_checker('ConstructLibrarySet', frame='object')
def audit_auxiliary_set_construct_library_set_files(value, system):
    '''
    [
        {
            "audit_description": "Auxiliary sets & construct library sets are expected to contain only sequence files or configuration files.",
            "audit_category": "unexpected files",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_auxiliary_set_construct_library_set_files)
    non_sequence_files = [file for file in value.get('files') if not (
        file.startswith('/sequence-files/') or file.startswith('/configuration-files/'))]
    if non_sequence_files and value.get('file_set_type', '') != 'cell sorting':
        non_sequence_files = ', '.join(
            [audit_link(path_to_text(file), file) for file in non_sequence_files])
        detail = (f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to '
                  f'`files` that are not sequence or configuration files: {non_sequence_files}.')
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
@audit_checker('AuxiliarySet', frame='object')
@audit_checker('ConstructLibrarySet', frame='object')
def audit_unexpected_virtual_samples(value, system):
    '''
    [
        {
            "audit_description": "Only curated sets, prediction sets and analysis sets are expected to link to virtual samples.",
            "audit_category": "unexpected sample",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_unexpected_virtual_samples)
    samples = []
    if 'samples' in value:
        samples = value.get('samples')
    if 'applied_to_samples' in value:
        samples = value.get('applied_to_samples')
    for sample in samples:
        sample_object = system.get('request').embed(sample)
        if sample_object.get('virtual'):
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to virtual sample '
                f'{audit_link(path_to_text(sample), sample)} in `samples`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('ConstructLibrarySet', frame='object')
@audit_checker('MeasurementSet', frame='object')
@audit_checker('AuxiliarySet', frame='object')
def audit_input_for(value, system):
    '''
    [
        {
            "audit_description": "Raw data sets with files are expected to be associated with at least one analysis set.",
            "audit_category": "missing analysis",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_input_for)
    if not value.get('input_for') and value.get('files'):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} is a raw data set with files, '
            f'but is not listed in any `input_file_sets` for any analysis sets.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
@audit_checker('ModelSet', frame='object')
def audit_inconsistent_location_files(value, system):
    '''
    [
        {
            "audit_description": "All files within this file set are expected to be hosted in the same location.",
            "audit_category": "inconsistent hosting locations",
            "audit_level": "ERROR"
        }
    ]
    '''

    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_inconsistent_location_files)
    externally_hosted_files = []
    local_files = []
    if 'files' in value:
        for file in value['files']:
            file_object = system.get('request').embed(file)

            if 'externally_hosted' in file_object:
                if file_object['externally_hosted']:
                    externally_hosted_files.append(file)
                else:
                    local_files.append(file)

    if externally_hosted_files and local_files:
        external_file_links = ','.join([audit_link(path_to_text(file), file) for file in externally_hosted_files])
        local_file_links = ','.join([audit_link(path_to_text(file), file) for file in local_files])
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has both externally hosted file(s): '
            f'{external_file_links}'
            f' and file(s) hosted on portal: '
            f'{local_file_links}.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
@audit_checker('AuxiliarySet', frame='object')
def audit_MPRA_read_names(value, system):
    '''
    [
        {
            "audit_description": "MPRA measurement set and auxiliary set sequence files are expected to specify a read name.",
            "audit_category": "missing read names",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "MPRA measurement set and auxiliary set sequence files are only expected to specify read names: Barcode forward, UMI, or Barcode reverse.",
            "audit_category": "inconsistent read names",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_missing = get_audit_message(audit_MPRA_read_names, index=0)
    audit_message_unexpected = get_audit_message(audit_MPRA_read_names, index=1)
    missing_read_names = []
    unexpected_read_names = []
    assays = set()
    if object_type == 'Measurement set':
        assay_term = value.get('assay_term')
        assay_term_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
        assays.add(assay_term_object.get('term_name'))
    elif object_type == 'Auxiliary set':
        measurement_sets = value.get('measurement_sets', [])
        for measurement_set in measurement_sets:
            measurement_set_object = system.get('request').embed(measurement_set, '@@object?skip_calculated=true')
            assay_term = measurement_set_object.get('assay_term')
            assay_term_object = system.get('request').embed(assay_term, '@@object?skip_calculated=true')
            assays.add(assay_term_object.get('term_name'))
    assays = list(assays)
    if any(assay for assay in assays if assay == 'massively parallel reporter assay'):
        if 'files' in value:
            sequence_files = [file for file in value['files'] if file.startswith('/sequence-files/')]
            for file in sequence_files:
                file_object = system.get('request').embed(file)
                read_names = file_object.get('read_names', '')
                if read_names:
                    if any(read_name not in ['Barcode forward', 'UMI', 'Barcode reverse'] for read_name in read_names):
                        unexpected_read_names.append(file)
                else:
                    missing_read_names.append(file)
    if missing_read_names:
        missing_read_names = ','.join([audit_link(path_to_text(file), file) for file in missing_read_names])
        detail = (
            f'MPRA {object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to sequence files: '
            f'{missing_read_names} that do not specify `read_names`.'
        )
        yield AuditFailure(audit_message_missing.get('audit_category', ''), f'{detail} {audit_message_missing.get("audit_description", "")}', level=audit_message_missing.get('audit_level', ''))
    if unexpected_read_names:
        unexpected_read_names = ','.join([audit_link(path_to_text(file), file) for file in unexpected_read_names])
        detail = (
            f'MPRA {object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to sequence files: '
            f'{unexpected_read_names} with `read_names` not associated with the MPRA uniform processing pipeline.'
        )
        yield AuditFailure(audit_message_unexpected.get('audit_category', ''), f'{detail} {audit_message_unexpected.get("audit_description", "")}', level=audit_message_unexpected.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
def audit_single_cell_read_names(value, system):
    '''
    [
        {
            "audit_description": "Sequence files are expected to have read names.",
            "audit_category": "missing read names",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Single cell assay measurement sets are only expected to have sequence files with read names: Read 1, Read 2, and Barcode index.",
            "audit_category": "unexpected read names",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    audit_message_missing_read_names = get_audit_message(audit_single_cell_read_names, index=0)
    audit_message_unexpected_read_names = get_audit_message(audit_single_cell_read_names, index=1)
    # Check read_names info on SeqFile objects from single cell MeaSet
    # Either sort the errors into missing or unexpected read names
    if single_cell_check(system, value, 'Measurement set'):
        if 'files' in value:
            missing_read_names = []
            unexpected_read_names = []
            for file in value['files']:
                if file.startswith('/sequence-files/'):
                    sequence_file_object = system.get('request').embed(file)
                    applicable_read_types = ['R1', 'R2', 'R3']  # Skip Index 1 and Index 2
                    # Get read type
                    illumina_read_type = sequence_file_object.get('illumina_read_type', '')
                    # If no read type or I-type, skip audit
                    if illumina_read_type not in applicable_read_types:
                        continue
                    # Check for read names
                    read_names = sequence_file_object.get('read_names', '')
                    if read_names:
                        if any(read_name not in ['Read 1', 'Read 2', 'Barcode index'] for read_name in read_names):
                            unexpected_read_names.append(file)
                    else:
                        missing_read_names.append(file)

        # Audit for missing read names
        if missing_read_names:
            for file in missing_read_names:
                detail = (
                    f'Measurement set {audit_link(path_to_text(value["@id"]), value["@id"])} has a sequence '
                    f'file {audit_link(path_to_text(file), file)} missing `read_names`.'
                )
                yield AuditFailure(audit_message_missing_read_names.get('audit_category', ''), f'{detail} {audit_message_missing_read_names.get("audit_description", "")}', level=audit_message_missing_read_names.get('audit_level', ''))
        # Audit for unexpected read names
        if unexpected_read_names:
            for file in unexpected_read_names:
                detail = (
                    f'Single cell Measurement Set {audit_link(path_to_text(value["@id"]), value["@id"])} has a sequence '
                    f'file {audit_link(path_to_text(file), file)} with `read_names` not associated with the single cell uniform processing '
                    f'pipeline.'
                )
                yield AuditFailure(audit_message_unexpected_read_names.get('audit_category', ''), f'{detail} {audit_message_unexpected_read_names.get("audit_description", "")}', level=audit_message_unexpected_read_names.get('audit_level', ''))


@audit_checker('FileSet', frame='object')
def audit_control_for_control_type(value, system):
    '''
    [
        {
            "audit_description": "File sets that are controls for other file sets are expected to define a control type.",
            "audit_category": "missing control type",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "File sets that specify a control type are expected to be a control for other file sets.",
            "audit_category": "missing control for",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_missing_control_type = get_audit_message(audit_control_for_control_type, index=0)
    audit_message_missing_control_for = get_audit_message(audit_control_for_control_type, index=1)
    if value.get('control_for', '') and not (value.get('control_type', '')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `control_type`.'
        )
        yield AuditFailure(audit_message_missing_control_type.get('audit_category', ''), f'{detail} {audit_message_missing_control_type.get("audit_description", "")}', level=audit_message_missing_control_type.get('audit_level', ''))
    elif value.get('control_type', '') and not (value.get('control_for', '')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `control_for`. The `control_file_sets` should be patched on '
            f'the file sets it serves as a control for and this property, `control_for`, '
            f'will be reverse calculated.'
        )
        yield AuditFailure(audit_message_missing_control_for.get('audit_category', ''), f'{detail} {audit_message_missing_control_for.get("audit_description", "")}', level=audit_message_missing_control_for.get('audit_level', ''))


@audit_checker('MeasurementSet', frame='object')
@audit_checker('AnalysisSet', frame='object')
def audit_inconsistent_controlled_access(value, system):
    '''
    [
        {
            "audit_description": "The files in a file set should be submitted with the same access restrictions as indicated by the institutional certificate covering the samples linked to the same file set.",
            "audit_category": "inconsistent controlled access",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "All files in a file set should be submitted with the same access restrictions as each other.",
            "audit_category": "inconsistent controlled access",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_file_sample = get_audit_message(audit_inconsistent_controlled_access, index=0)
    audit_message_mixed_files = get_audit_message(audit_inconsistent_controlled_access, index=1)

    formats_to_check = ['bam', 'cram', 'fastq']
    files_by_access = {}
    files = value.get('files', [])
    for file in files:
        file_object = system.get('request').embed(file, '@@object_with_select_calculated_properties?field=@id')
        if file_object.get('file_format', '') in formats_to_check \
                and not file_object.get('redacted', None) \
                and file_object.get('controlled_access', None) is not None:
            if file_object.get('controlled_access', None) not in files_by_access:
                files_by_access[file_object.get('controlled_access', None)] = [file_object.get('@id')]
            else:
                files_by_access[file_object.get('controlled_access', None)].append(file_object.get('@id'))

    if True in files_by_access and False in files_by_access:
        controlled_access_of_files_phrase = 'controlled and uncontrolled access'
        # Mixed controlled access is only unexpected for Meas Sets
        if 'MeasurementSet' in value.get('@type', []):
            controlled_files_link = ', '.join([audit_link(path_to_text(file), file) for file in files_by_access[True]])
            uncontrolled_files_link = ', '.join([audit_link(path_to_text(file), file)
                                                for file in files_by_access[False]])
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} contains '
                f'files {controlled_files_link} submitted as controlled access and files {uncontrolled_files_link} '
                f'submitted as uncontrolled access.'
            )
            yield AuditFailure(
                audit_message_mixed_files.get('audit_category', ''),
                f'{detail} {audit_message_mixed_files.get("audit_description", "")}',
                level=audit_message_mixed_files.get('audit_level', '')
            )
    elif True in files_by_access and False not in files_by_access:
        controlled_access_of_files_phrase = 'controlled access'
        controlled_files_link = ', '.join([audit_link(path_to_text(file), file) for file in files_by_access[True]])
        uncontrolled_files_link = ''
    else:
        controlled_access_of_files_phrase = 'uncontrolled access'
        controlled_files_link = ''
        uncontrolled_files_link = ', '.join([audit_link(path_to_text(file), file)
                                             for file in files_by_access[False]])

    samples = value.get('samples', [])
    for sample in samples:
        sample_object = system.get('request').embed(
            sample, '@@object_with_select_calculated_properties?field=institutional_certificates&field=@id')
        for ic in sample_object.get('institutional_certificates'):
            ic_object = system.get('request').embed(ic, '@@object_with_select_calculated_properties?field=@id')
            if any(ic_object.get('controlled_access') != access for access in files_by_access):
                if ic_object.get('controlled_access') is True:
                    controlled_access_of_ic_phrase = 'controlled access'
                else:
                    controlled_access_of_ic_phrase = 'uncontrolled access'
                file_links_phrase = ''
                if controlled_access_of_files_phrase == 'controlled and uncontrolled access':
                    file_links_phrase = f'{controlled_files_link} and {uncontrolled_files_link} respectively'
                elif controlled_access_of_files_phrase == 'controlled access':
                    file_links_phrase = f'{controlled_files_link}'
                else:
                    file_links_phrase = f'{uncontrolled_files_link}'
                detail = (
                    f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
                    f'contains {controlled_access_of_files_phrase} files {file_links_phrase}, but the '
                    f'sample {audit_link(path_to_text(sample_object["@id"]), sample_object["@id"])} '
                    f'is covered by institutional certificate {audit_link(ic_object["certificate_identifier"], ic_object["@id"])} '
                    f'which requires {controlled_access_of_ic_phrase}.'
                )
                yield AuditFailure(
                    audit_message_file_sample.get('audit_category', ''),
                    f'{detail} {audit_message_file_sample.get("audit_description", "")}',
                    level=audit_message_file_sample.get('audit_level', '')
                )


@audit_checker('FileSet', frame='object')
def audit_file_set_missing_publication(value, system):
    '''
    [
        {
            "audit_description": "Released and archived file sets are expected to be associated with a publication.",
            "audit_category": "missing publication",
            "audit_level": "INTERNAL_ACTION"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_file_set_missing_publication, index=0)
    if value.get('status') in ['released', 'archived'] and not (value.get('publications')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `publications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
