from snovault.auditor import (
    AuditFailure,
    audit_checker
)

from snovault.mapping import watch_for_changes_in

from .formatter import (
    audit_link,
    path_to_text,
    get_audit_message,
    space_in_words,
    join_obj_paths
)

# Single cell assay terms

SINGLE_CELL_ASSAY_TERMS = {'/assay-terms/OBI_0002762/': 'single-nucleus ATAC-seq',
                           '/assay-terms/OBI_0003109/': 'single-nucleus RNA sequencing assay',
                           '/assay-terms/OBI_0002631/': 'single-cell RNA sequencing assay',
                           '/assay-terms/OBI_0002764/': 'single-cell ATAC-seq',
                           }

# Gene expression assay terms
TRANSCRIPT_ASSAY_TERMS = ['/assay-terms/OBI_0003090/',  # bulk RNA-seq assay
                          '/assay-terms/OBI_0002631/',  # single-cell RNA sequencing assay
                          '/assay-terms/OBI_0003109/',  # single-nucleus RNA sequencing assay
                          '/assay-terms/OBI_0003660/',  # in vitro CRISPR screen using single-cell RNA-seq
                          '/assay-terms/OBI_0003662/',  # single-nucleus methylcytosine and transcriptome sequencing assay
                          '/assay-terms/NTR_0000761/',  # spatial transcriptomics
                          '/assay-terms/NTR_0000735/'   # single cell nascent transcription sequencing
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


def single_cell_check(system, value, object_type, single_cell_assay_terms=list(SINGLE_CELL_ASSAY_TERMS.keys()), include_perturb_seq=False):
    if include_perturb_seq:
        # in vitro CRISPR screen using single-cell RNA-seq: '/assay-terms/OBI_0003660/'
        # in vitro CRISPR screen using single-cell ATAC-seq: '/assay-terms/NTR_0000798/'
        single_cell_assay_terms = single_cell_assay_terms + ['/assay-terms/OBI_0003660/', '/assay-terms/NTR_0000798/']
    if object_type == 'Measurement set':
        assay_term = value.get('assay_term')
        return assay_term in single_cell_assay_terms
    elif object_type == 'Auxiliary set':
        measurement_sets = value.get('measurement_sets', [])
        for measurement_set in measurement_sets:
            measurement_set_obj = system.get('request').embed(measurement_set, '@@object?skip_calculated=true')
            assay_term = measurement_set_obj.get('assay_term')
            if assay_term in single_cell_assay_terms:
                return True
        return False
    elif object_type == 'Construct library set':
        samples = value.get('samples', [])
        for sample in samples:
            sample_obj = system.get('request').embed(
                sample, '@@object_with_select_calculated_properties?field=file_sets')
            file_sets = sample_obj.get('file_sets', [])
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
    preferred_assay_titles = value.get('preferred_assay_titles', [])

    # Skip audit for specific Measurement set + assay combinations
    skip_assays = [
        'Variant painting via immunostaining',
        'Variant painting via fluorescence',
        'Cell painting'
    ]
    if object_type == 'Measurement set' and any(t in skip_assays for t in preferred_assay_titles):
        return

    audit_message_missing_files = get_audit_message(audit_no_files, index=0)
    if not value.get('files', '') and object_type != 'Construct library set':
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `files`.'
        )
        yield AuditFailure(
            audit_message_missing_files.get('audit_category', ''),
            f'{detail} {audit_message_missing_files.get("audit_description", "")}',
            level=audit_message_missing_files.get('audit_level', '')
        )


def audit_missing_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Sequence files in a file set associated with non-single cell data are expected to link to a sequence specification document.",
            "audit_category": "missing sequence specification",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Sequence files in a file set associated with single cell data are expected to link to a sequence specification file.",
            "audit_category": "missing sequence specification",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    if value['file_set_type'] == 'guide library':
        # guide construct library set sequence files are not expected to specfiy seqspec
        return
    if 'files' in value:
        # Check single cell status
        is_single_cell = single_cell_check(system, value, object_type, include_perturb_seq=True)
        no_seqspec = []  # For Audit 1
        no_seqspec_doc = []  # For Audit 2
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file, '@@object?skip_calculated=true')
                platform_object = system.get('request').embed(sequence_file_object.get(
                    'sequencing_platform'), '@@object?skip_calculated=true')
                if sequence_file_object.get('file_format') == 'pod5' or \
                        platform_object.get('company', '') == 'Oxford Nanopore Technologies':
                    continue
                # Overall audit: if a SeqFile has no seqspec ConfigFile
                if not sequence_file_object.get('seqspecs'):
                    # Audit 1: For single cell, we expect seqspecs to be ConfigFiles
                    if is_single_cell:
                        no_seqspec.append(file)
                    # Audit 2: For non-single cell, we expect seqspecs to be seqspec_document
                    else:
                        if not sequence_file_object.get('seqspec_document'):
                            no_seqspec_doc.append(file)
        # Audit 1: Single cell SeqFiles are expected linked to ConfigFile seqspecs
        if no_seqspec:
            audit_message = get_audit_message(audit_missing_seqspec, index=1)
            no_seqspec_paths = join_obj_paths(data_object_paths=no_seqspec)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{no_seqspec_paths} which do not have any `seqspecs`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))
        # Audit 2: Check if non-single cell SeqFiles without seqspec ConfigFile still have seqspec_document.
        if no_seqspec_doc:
            # Get audit message for missing seqspec_document
            no_seqspec_doc_paths = join_obj_paths(data_object_paths=no_seqspec_doc)
            audit_message = get_audit_message(audit_missing_seqspec, index=0)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{no_seqspec_doc_paths} which do not have a `seqspec_document`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_unexpected_seqspec(value, system):
    '''
    [
        {
            "audit_description": "Pod5 sequence files in a file set should not be linked to a sequence specification file.",
            "audit_category": "unexpected sequence specification",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Sequence files should not have both `seqspecs` and `seqspec_document`.",
            "audit_category": "unexpected sequence specification",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Non-single cell sequence files are expected to link to a Document with `document_type` library structure seqspec.",
            "audit_category": "unexpected sequence specification",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    has_seqspec = []    # For Audit 1
    had_duo_seqspecs = []   # For Audit 2
    has_seqspec_document = []   # For Audit 3
    if 'files' in value:
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)
                # Audit 1: Pod5 sequence files should not be linked to a seqspec
                if sequence_file_object.get('file_format') == 'pod5' and sequence_file_object.get('seqspecs'):
                    has_seqspec.append(file)
                # Audit 2: SeqFiles should not have both seqspec_of and seqspec_document
                elif sequence_file_object.get('seqspecs') and sequence_file_object.get('seqspec_document'):
                    had_duo_seqspecs.append(file)
                # Audit 3: SeqFiles should link to library structure seqspec document
                elif not sequence_file_object.get('seqspecs') and sequence_file_object.get('seqspec_document'):
                    has_seqspec_document.append(file)

        # Audit message for Audit 1
        if has_seqspec:
            audit_message_pod5 = get_audit_message(audit_unexpected_seqspec, index=0)
            has_seqspec_paths = join_obj_paths(data_object_paths=has_seqspec)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has pod5 sequence file(s): '
                f'{has_seqspec_paths} which are linked to a seqspec.'
            )
            yield AuditFailure(audit_message_pod5.get('audit_category', ''), f'{detail} {audit_message_pod5.get("audit_description", "")}', level=audit_message_pod5.get('audit_level', ''))

        # Audit message for Audit 2
        if had_duo_seqspecs:
            audit_msg_double_seqspec = get_audit_message(audit_unexpected_seqspec, index=1)
            had_duo_seqspecs_paths = join_obj_paths(data_object_paths=had_duo_seqspecs)
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                f'{had_duo_seqspecs_paths} which are linked to both sequence specification files as Configuration File and library structure seqspec as Document.'
            )
            yield AuditFailure(audit_msg_double_seqspec.get('audit_category', ''), f'{detail} {audit_msg_double_seqspec.get("audit_description", "")}', level=audit_msg_double_seqspec.get('audit_level', ''))

        # Audit message for Audit 3
        if has_seqspec_document:
            wrong_documents = []
            for seqfile in has_seqspec_document:
                # Get file obj to get to seqspec doc
                seqfile_obj = system.get('request').embed(seqfile + '@@object?skip_calculated=true')
                # Get to document obj to get doc type
                document_obj = system.get('request').embed(seqfile_obj.get(
                    'seqspec_document') + '@@object?skip_calculated=true')
                if document_obj.get('document_type') != 'library structure seqspec':
                    wrong_documents.append(seqfile)
            # Output error msg if there are wrong document types used
            if wrong_documents:
                wrong_document_paths = join_obj_paths(data_object_paths=wrong_documents)
                audit_msg_wrong_seqspec_doc = get_audit_message(audit_unexpected_seqspec, index=2)
                detail = (
                    f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} has sequence file(s): '
                    f'{wrong_document_paths} which link to a `seqspec_document` that is not a library structure seqspec document.'
                )
                yield AuditFailure(audit_msg_wrong_seqspec_doc.get('audit_category', ''), f'{detail} {audit_msg_wrong_seqspec_doc.get("audit_description", "")}', level=audit_msg_wrong_seqspec_doc.get('audit_level', ''))


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
    # Non-sc seqspec submitted through file sets should still be audited like single cells
    if 'files' in value:
        for file in value['files']:
            # Audit 1: Seqspec have seqspec_of files that are not in the same file set as the seqspec
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

            # Audit 2: the file set with a seqspec configuration file without the associated sequence files also in the file set.
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

    # Set up lookup ref as {seq_set_key: {seq_file: set(seqspecs)}}
    if 'files' in value:
        sequence_to_seqspec = {}
        for file in value['files']:
            if file.startswith('/sequence-files/'):
                sequence_file_object = system.get('request').embed(file)
                sequencing_run = str(sequence_file_object.get('sequencing_run'))
                flowcell_id = sequence_file_object.get('flowcell_id', '')
                lane = str(sequence_file_object.get('lane', ''))
                index = sequence_file_object.get('index', '')
                seq_set_identifies = [sequencing_run, flowcell_id, lane, index]
                key_list = [item for item in seq_set_identifies if item != '']
                key = ':'.join(key_list)    # combined run, flowcell, lane, index as identifiers
                if key not in sequence_to_seqspec:
                    sequence_to_seqspec[key] = {file: set(sequence_file_object.get('seqspecs', []))}
                else:
                    sequence_to_seqspec[key][file] = set(sequence_file_object.get('seqspecs', []))

        # Audit 1: If seqfiles from the same sequencing set have different seqspecs, flag it
        # Single cell or not, this audit should stay for all SeqFiles
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

        # Audit 2: If the same seqspec is linked to different sequencing sets, flag it
        # now limit it to single cell only
        if not single_cell_check(system, value, object_type, include_perturb_seq=False):
            return

        seqspec_to_sequence = {}    # {list_of_seqspec_as_str: [(seq_set_key, seq_file)]}
        for key, file_dict in sequence_to_seqspec.items():
            for file, seqspec in file_dict.items():
                if seqspec:
                    seqspec_str_formatted = ':'.join(sorted(seqspec))
                    if seqspec_str_formatted not in seqspec_to_sequence:
                        seqspec_to_sequence[seqspec_str_formatted] = [(key, file)]
                    else:
                        seqspec_to_sequence[seqspec_str_formatted].append((key, file))

        for seqspec, sequence_files in seqspec_to_sequence.items():
            key_set = set()
            for key, file in sequence_files:    # key here is seq_set_key
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
    file_info = {}
    for file in value.get('files', []):
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
        if single_cell_check(system, value, object_type, include_perturb_seq=True):
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
    non_sequence_files = [file for file in value.get('files', []) if not (
        file.startswith('/sequence-files/') or file.startswith('/configuration-files/'))]
    if non_sequence_files and value.get('file_set_type', '') != 'cell sorting':
        non_sequence_files = ', '.join(
            [audit_link(path_to_text(file), file) for file in non_sequence_files])
        detail = (f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to '
                  f'`files` that are not sequence or configuration files: {non_sequence_files}.')
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
    for sample in samples:
        sample_object = system.get('request').embed(sample)
        if sample_object.get('virtual'):
            detail = (
                f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} links to virtual sample '
                f'{audit_link(path_to_text(sample), sample)} in `samples`.'
            )
            yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


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
        assay_titles = value.get('assay_titles', [])
        assays.update(assay_titles)
    elif object_type == 'Auxiliary set':
        assay_titles = value.get('assay_titles', [])
        assays.update(assay_titles)
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
    if single_cell_check(system, value, 'Measurement set', include_perturb_seq=False):
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
    if value.get('control_for', []) and not (value.get('control_types', [])):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `control_types`.'
        )
        yield AuditFailure(audit_message_missing_control_type.get('audit_category', ''), f'{detail} {audit_message_missing_control_type.get("audit_description", "")}', level=audit_message_missing_control_type.get('audit_level', ''))
    elif value.get('control_types', []) and not (value.get('control_for', [])):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `control_for`. The `control_file_sets` should be patched on '
            f'the file sets it serves as a control for and this property, `control_for`, '
            f'will be reverse calculated.'
        )
        yield AuditFailure(audit_message_missing_control_for.get('audit_category', ''), f'{detail} {audit_message_missing_control_for.get("audit_description", "")}', level=audit_message_missing_control_for.get('audit_level', ''))


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

    if not files:
        return

    for file in files:
        file_object = system.get('request').embed(file, '@@object_with_select_calculated_properties?field=@id')
        if file_object.get('file_format', '') in formats_to_check \
                and not file_object.get('redacted', None) \
                and file_object.get('controlled_access', None) is not None:
            if file_object.get('controlled_access', None) not in files_by_access:
                files_by_access[file_object.get('controlled_access', None)] = [file_object.get('@id')]
            else:
                files_by_access[file_object.get('controlled_access', None)].append(file_object.get('@id'))

    controlled_files_link = ''
    uncontrolled_files_link = ''
    controlled_access_of_files_phrase = ''
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
    elif True not in files_by_access and False in files_by_access:
        controlled_access_of_files_phrase = 'uncontrolled access'
        controlled_files_link = ''
        uncontrolled_files_link = ', '.join([audit_link(path_to_text(file), file)
                                             for file in files_by_access[False]])

    samples = value.get('samples', [])
    for sample in samples:
        sample_object = system.get('request').embed(
            sample, '@@object_with_select_calculated_properties?field=institutional_certificates&field=@id')
        for ic in sample_object.get('institutional_certificates', []):
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
    if object_type != 'Curated set' and value.get('status') in ['released', 'archived'] and not (value.get('publications', [])):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `publications`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_file_set_files_missing_analysis_step_version(value, system):
    '''
    [
        {
            "audit_description": "Analysis set and prediction set files are expected to specify analysis step version.",
            "audit_category": "missing analysis step version",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Model set files are expected to specify analysis step version.",
            "audit_category": "missing analysis step version",
            "audit_level": "WARNING"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_analysis_prediction = get_audit_message(audit_file_set_files_missing_analysis_step_version, index=0)
    audit_message_model = get_audit_message(audit_file_set_files_missing_analysis_step_version, index=1)
    if object_type == 'Model set':
        audit_message = audit_message_model
    else:
        audit_message = audit_message_analysis_prediction
    files = value.get('files')
    files_with_missing_asv = []
    for file in files:
        file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
        if file_object.get('derived_manually') is True:
            continue
        else:
            if not (file_object.get('analysis_step_version', '')):
                files_with_missing_asv.append(file)
    if files_with_missing_asv:
        files_with_missing_asv = ', '.join([audit_link(path_to_text(file), file) for file in files_with_missing_asv])
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {files_with_missing_asv} that are missing `analysis_step_version`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


def audit_input_file_sets_derived_from(value, system):
    '''
    [
        {
            "audit_description": "The file sets of the files that are used to derive the files in this file set are expected to be listed in the input file sets.",
            "audit_category": "missing input file set",
            "audit_level": "ERROR"
        },
        {
            "audit_description": "Files in an analysis set are expected to be derived from other files.",
            "audit_category": "missing derived from",
            "audit_level": "NOT_COMPLIANT"
        },
        {
            "audit_description": "Files in prediction sets and model sets are expected to be derived from other files.",
            "audit_category": "missing derived from",
            "audit_level": "WARNING"
        },
        {
            "audit_description": "The input files are expected to belong to the input file sets.",
            "audit_category": "unexpected input file set",
            "audit_level": "ERROR"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message_missing_input_file_set = get_audit_message(audit_input_file_sets_derived_from, index=0)
    audit_message_missing_derived_from_analysis = get_audit_message(audit_input_file_sets_derived_from, index=1)
    audit_message_missing_derived_from_prediction_model = get_audit_message(audit_input_file_sets_derived_from, index=2)
    audit_message_unexpected_input_file_set = get_audit_message(audit_input_file_sets_derived_from, index=3)
    detail = ''
    input_file_sets = value.get('input_file_sets', [])
    files = value.get('files', [])
    files_to_link = []
    derived_from_files_to_link = []
    missing_derived_from_file_sets = []
    missing_derived_from = []
    all_derived_from_file_sets = []
    if files:
        for file in files:
            file_object = system.get('request').embed(file + '@@object?skip_calculated=true')
            derived_from_files = file_object.get('derived_from', [])
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
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {files_to_link} that are `derived_from` '
            f'file(s) {derived_from_files_to_link} from file set(s) {missing_derived_from_file_sets} '
            f'which are not in `input_file_sets`.'
        )
        yield AuditFailure(audit_message_missing_input_file_set.get('audit_category', ''), f'{detail} {audit_message_missing_input_file_set.get("audit_description", "")}', level=audit_message_missing_input_file_set.get('audit_level', ''))
    if missing_derived_from:
        if object_type == 'Analysis set':
            audit_message_missing_derived_from = audit_message_missing_derived_from_analysis
        else:
            audit_message_missing_derived_from = audit_message_missing_derived_from_prediction_model
        missing_derived_from = ', '.join([audit_link(path_to_text(file), file) for file in missing_derived_from])
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file(s) {missing_derived_from} that have no `derived_from`.'
        )
        yield AuditFailure(audit_message_missing_derived_from.get('audit_category', ''), f'{detail} {audit_message_missing_derived_from.get("audit_description", "")}', level=audit_message_missing_derived_from.get('audit_level', ''))
    unexpected_file_sets = list(set(input_file_sets) - set(all_derived_from_file_sets))
    if unexpected_file_sets:
        unexpected_file_sets = ', '.join(
            [audit_link(path_to_text(file_set), file_set) for file_set in unexpected_file_sets])
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'links to file set(s): {unexpected_file_sets} in `input_file_sets` that are not represented in the '
            f'`derived_from` of the file sets of the files in this analysis.'
        )
        yield AuditFailure(audit_message_unexpected_input_file_set.get('audit_category', ''), f'{detail} {audit_message_unexpected_input_file_set.get("audit_description", "")}', level=audit_message_unexpected_input_file_set.get('audit_level', ''))


def audit_file_set_missing_description(value, system):
    '''
    [
        {
            "audit_description": "Principal analysis sets, prediction sets, and model sets are expected to have descriptions summarizing the experiment or predictive model they are associated with.",
            "audit_category": "missing description",
            "audit_level": "NOT_COMPLIANT"
        }
    ]
    '''
    object_type = space_in_words(value['@type'][0]).capitalize()
    audit_message = get_audit_message(audit_file_set_missing_description, index=0)
    if value.get('file_set_type') != 'intermediate analysis' and not (value.get('description')):
        detail = (
            f'{object_type} {audit_link(path_to_text(value["@id"]), value["@id"])} '
            f'has no `description`.'
        )
        yield AuditFailure(audit_message.get('audit_category', ''), f'{detail} {audit_message.get("audit_description", "")}', level=audit_message.get('audit_level', ''))


function_dispatcher_file_set_object = {
    'audit_no_files': audit_no_files,
    'audit_inconsistent_sequencing_kit': audit_inconsistent_sequencing_kit,
    'audit_control_for_control_type': audit_control_for_control_type,
    'audit_file_set_missing_publication': audit_file_set_missing_publication
}

function_dispatcher_measurement_set_object = {
    'audit_missing_seqspec': audit_missing_seqspec,
    'audit_unexpected_seqspec': audit_unexpected_seqspec,
    'audit_files_associated_with_incorrect_fileset': audit_files_associated_with_incorrect_fileset,
    'audit_inconsistent_seqspec': audit_inconsistent_seqspec,
    'audit_unexpected_virtual_samples': audit_unexpected_virtual_samples,
    'audit_input_for': audit_input_for,
    'audit_inconsistent_location_files': audit_inconsistent_location_files,
    'audit_MPRA_read_names': audit_MPRA_read_names,
    'audit_single_cell_read_names': audit_single_cell_read_names,
    'audit_inconsistent_controlled_access': audit_inconsistent_controlled_access
}

function_dispatcher_auxiliary_set_object = {
    'audit_missing_seqspec': audit_missing_seqspec,
    'audit_unexpected_seqspec': audit_unexpected_seqspec,
    'audit_files_associated_with_incorrect_fileset': audit_files_associated_with_incorrect_fileset,
    'audit_inconsistent_seqspec': audit_inconsistent_seqspec,
    'audit_auxiliary_set_construct_library_set_files': audit_auxiliary_set_construct_library_set_files,
    'audit_unexpected_virtual_samples': audit_unexpected_virtual_samples,
    'audit_input_for': audit_input_for,
    'audit_MPRA_read_names': audit_MPRA_read_names
}

function_dispatcher_construct_library_set_object = {
    'audit_missing_seqspec': audit_missing_seqspec,
    'audit_unexpected_seqspec': audit_unexpected_seqspec,
    'audit_files_associated_with_incorrect_fileset': audit_files_associated_with_incorrect_fileset,
    'audit_inconsistent_seqspec': audit_inconsistent_seqspec,
    'audit_loci_valid_chrom_sizes': audit_loci_valid_chrom_sizes,
    'audit_auxiliary_set_construct_library_set_files': audit_auxiliary_set_construct_library_set_files,
    'audit_unexpected_virtual_samples': audit_unexpected_virtual_samples,
    'audit_input_for': audit_input_for
}

function_dispatcher_analysis_set_object = {
    'audit_inconsistent_controlled_access': audit_inconsistent_controlled_access,
    'audit_input_file_sets_derived_from': audit_input_file_sets_derived_from,
    'audit_file_set_files_missing_analysis_step_version': audit_file_set_files_missing_analysis_step_version,
    'audit_file_set_missing_description': audit_file_set_missing_description
}

function_dispatcher_prediction_set_object = {
    'audit_loci_valid_chrom_sizes': audit_loci_valid_chrom_sizes,
    'audit_input_file_sets_derived_from': audit_input_file_sets_derived_from,
    'audit_file_set_files_missing_analysis_step_version': audit_file_set_files_missing_analysis_step_version,
    'audit_file_set_missing_description': audit_file_set_missing_description
}

function_dispatcher_model_set_object = {
    'audit_inconsistent_location_files': audit_inconsistent_location_files,
    'audit_input_file_sets_derived_from': audit_input_file_sets_derived_from,
    'audit_file_set_files_missing_analysis_step_version': audit_file_set_files_missing_analysis_step_version,
    'audit_file_set_missing_description': audit_file_set_missing_description
}


@audit_checker('FileSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_file_set_object.values()))
def audit_file_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_file_set_object.keys():
        for failure in function_dispatcher_file_set_object[function_name](value, system):
            yield failure


@audit_checker('MeasurementSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_measurement_set_object.values()))
def audit_measurement_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_measurement_set_object.keys():
        for failure in function_dispatcher_measurement_set_object[function_name](value, system):
            yield failure


@audit_checker('AuxiliarySet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_auxiliary_set_object.values()))
def audit_auxiliary_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_auxiliary_set_object.keys():
        for failure in function_dispatcher_auxiliary_set_object[function_name](value, system):
            yield failure


@audit_checker('ConstructLibrarySet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_construct_library_set_object.values()))
def audit_construct_library_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_construct_library_set_object.keys():
        for failure in function_dispatcher_construct_library_set_object[function_name](value, system):
            yield failure


@audit_checker('AnalysisSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_analysis_set_object.values()))
def audit_analysis_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_analysis_set_object.keys():
        for failure in function_dispatcher_analysis_set_object[function_name](value, system):
            yield failure


@audit_checker('PredictionSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_prediction_set_object.values()))
def audit_prediction_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_prediction_set_object.keys():
        for failure in function_dispatcher_prediction_set_object[function_name](value, system):
            yield failure


@audit_checker('ModelSet', frame='object')
@watch_for_changes_in(functions=list(function_dispatcher_model_set_object.values()))
def audit_model_set_object_dispatcher(value, system):
    for function_name in function_dispatcher_model_set_object.keys():
        for failure in function_dispatcher_model_set_object[function_name](value, system):
            yield failure
