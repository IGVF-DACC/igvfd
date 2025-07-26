from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path

from .base import (
    Item,
    paths_filtered_by_status
)

from datetime import datetime


def get_donors_from_samples(request, samples):
    donor_objects = []
    for sample in samples:
        donor_objects += request.embed(sample, '@@object').get('donors', [])
    return sorted(set(donor_objects))


def get_file_objs_from_files(request, files):
    '''Get file objects from an array of files'''
    file_objs = []
    if files is not None:
        for file in files:
            file_objs.append(request.embed(file, '@@object?skip_calculated=true'))
    return file_objs


def get_assessed_gene_symbols(request, assessed_genes=None):
    '''Get gene symbols from an array of assessed genes.'''
    if not assessed_genes:
        return ''
    else:
        gene_symbols = []
        for assessed_gene in assessed_genes:
            gene_symbols.append(request.embed(
                assessed_gene, '@@object?skip_calculated=true').get('symbol', ''))
        return ', '.join(sorted(gene_symbols))


def get_assessed_gene_phrase(request, assessed_genes=None):
    """Get the assessed gene phrase from assessed_genes. If more than 5, return the number of assessed genes.
    """
    len_assessed_genes = len(assessed_genes) if assessed_genes else 0
    if len_assessed_genes > 5:
        assessed_gene_phrase = f'{len_assessed_genes} assessed genes'
    else:
        assessed_gene_phrase = get_assessed_gene_symbols(request, assessed_genes)
    return assessed_gene_phrase


def get_cls_phrase(cls_set, only_cls_input=False):
    cls_set = sorted(cls_set)
    cls_phrases = []
    for summary in cls_set:
        article = 'a'
        if any(summary.startswith(x) for x in ['a', 'e', 'i', 'o', 'u']):
            article = 'an'
        if only_cls_input:
            cls_phrases.append(f'{summary[0].lower()}{summary[1:]}')
        else:
            cls_phrases.append(f'{article} {summary[0].lower()}{summary[1:]}')
    if len(cls_phrases) == 1:
        cls_phrase = cls_phrases[0]
    elif len(cls_phrases) == 2:
        cls_phrase = ' and '.join(cls_phrases)
    # make special case for SGE assays: >20 CLS under each analysis set
    elif len(cls_phrases) > 2:
        if cls_phrases[0].startswith('an editing template library'):
            common_phrase = cls_phrases[0].split(' in ')[0]
            # only condense sentence if all CLS have the same selection criteria (i.e. sequence variants)
            if all(cls_phrase.startswith(common_phrase) for cls_phrase in cls_phrases):
                targeton_dict = {}
                for cls_phrase in cls_phrases:
                    # e.g. editing template library targeting sequence variants in exon6B of BARD1
                    gene = cls_phrase.split(' ')[-1]
                    targeton = cls_phrase.split(' ')[-3]
                    if gene not in targeton_dict:
                        targeton_dict[gene] = set([targeton])
                    else:
                        targeton_dict[gene].add(targeton)
                cls_count_phrases = []
                for gene, targetons in targeton_dict.items():
                    cls_count_phrases.append(f'in {len(targetons)} targetons of {gene}')
                cls_phrase = common_phrase.replace('an ', '').replace(
                    'library', 'libraries') + ' ' + ', '.join(cls_count_phrases)
            else:
                cls_phrase = ', '.join(cls_phrases[:-1]) + ', and ' + cls_phrases[-1]
        else:
            cls_phrase = ', '.join(cls_phrases[:-1]) + ', and ' + cls_phrases[-1]
    if not only_cls_input:
        # Do not add "integrating" when all input file sets are CLS.
        cls_phrase = f'integrating {cls_phrase}'
    return cls_phrase


@abstract_collection(
    name='file-sets',
    unique_key='accession',
    properties={
        'title': 'File Sets',
        'description': 'Listing of file sets',
    }
)
class FileSet(Item):
    item_type = 'file_set'
    base_types = ['FileSet'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file_set.json')
    rev = {
        'files': ('File', 'file_set'),
        'control_for': ('FileSet', 'control_file_sets'),
        'input_for': ('FileSet', 'input_file_sets')
    }
    embedded_with_frame = [
        Path('award.contact_pi', include=['@id', 'contact_pi', 'component', 'title']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases', 'assembly', 'content_type', 'controlled_access', 'derived_from',
             'file_format', 'file_size', 'href', 'md5sum', 's3_uri', 'submitted_file_name', 'status', 'transcriptome_annotation',
                               'creation_timestamp', 'sequencing_platform', 'upload_status', 'submitted_file_name']),
        Path('control_for', include=['@id', 'accession', 'aliases', 'status']),
        Path('donors', include=['@id', 'accession', 'aliases', 'sex', 'status', 'strain_background', 'taxa']),
        Path('samples.sample_terms', include=[
            '@id',
            '@type',
            'accession',
            'aliases',
            'treatments',
            'cellular_sub_pool',
            'classifications',
            'disease_terms',
            'modifications',
            'sample_terms',
            'status',
            'summary',
            'targeted_sample_term',
            'taxa',
            'term_name',
            'treatments',
            'institutional_certificates',
        ]),
        Path('samples.disease_terms', include=['@id', 'term_name', 'status']),
        Path('samples.targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('samples.modifications', include=['@id', 'modality', 'status']),
        Path('samples.treatments', include=['@id', 'treatment_term_name',
             'purpose', 'treatment_type', 'summary', 'status']),
        Path('samples.institutional_certificates', include=['@id',
             'certificate_identifier', 'status', 'data_use_limitation', 'data_use_limitation_modifiers', 'controlled_access']),
        Path('construct_library_sets.integrated_content_files', include=[
             '@id', 'accession', 'file_set_type', 'summary', 'status', 'content_type', 'integrated_content_files']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
    ]

    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
        'samples',
        'samples.sample_terms',
        'samples.disease_terms',
        'samples.treatments',
        'samples.modifications',
        'donors',
    ]

    set_status_up = [
        'documents',
        'files',
        'input_file_sets',
        'samples'
    ]
    set_status_down = [
    ]

    @calculated_property(schema={
        'title': 'Files',
        'type': 'array',
        'description': 'The files associated with this file set.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File',
            'type': 'string',
            'linkFrom': 'File.file_set',
        },
        'notSubmittable': True
    })
    def files(self, request, files):
        return paths_filtered_by_status(request, files)

    @calculated_property(schema={
        'title': 'File Sets Controlled By This File Set',
        'type': 'array',
        'description': 'The file sets for which this file set is a control.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File Set Controlled By This File Set',
            'type': 'string',
            'linkFrom': 'FileSet.control_file_sets',
        },
        'notSubmittable': True
    })
    def control_for(self, request, control_for):
        return paths_filtered_by_status(request, control_for)

    @calculated_property(schema={
        'title': 'Submitted Files Timestamp',
        'description': 'The timestamp the first file object in the file_set or associated auxiliary sets was created.',
        'comment': 'Do not submit. The timestamp is automatically calculated.',
        'type': 'string',
        'format': 'date-time',
        'notSubmittable': True
    })
    def submitted_files_timestamp(self, request, files, auxiliary_sets=None):
        if auxiliary_sets is None:
            auxiliary_sets = []
        timestamps = set()
        files_to_traverse = []
        if files:
            files_to_traverse.extend(files)
        if auxiliary_sets:
            for auxiliary_set in auxiliary_sets:
                aux_set_object = request.embed(auxiliary_set, '@@object_with_select_calculated_properties?field=files')
                if 'files' in aux_set_object:
                    files_to_traverse.extend(aux_set_object['files'])
        for current_file_path in files_to_traverse:
            file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
            timestamp = file_object.get('creation_timestamp', None)
            if timestamp:
                timestamps.add(timestamp)
        if timestamps:
            res = sorted(timestamps, key=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z'))
            return res[0]

    @calculated_property(schema={
        'title': 'Input For',
        'description': 'The file sets that use this file set as an input.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input For',
            'type': 'string',
            'linkFrom': 'FileSet.input_file_sets',
        },
        'notSubmittable': True
    })
    def input_for(self, request, input_for):
        return paths_filtered_by_status(request, input_for)

    @calculated_property(
        define=True,
        condition='samples',
        schema={
            'title': 'Construct Library Sets',
            'description': 'The construct library sets associated with the samples of this file set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Construct Library Set',
                'description': 'A construct library set associated with a sample of this file set.',
                'type': 'string',
                'linkTo': 'FileSet',
            },
            'notSubmittable': True
        })
    def construct_library_sets(self, request, samples=None):
        construct_library_sets = set()
        for sample in samples:
            sample_object = request.embed(sample,
                                          '@@object_with_select_calculated_properties?'
                                          'field=construct_library_sets'
                                          )
            if sample_object.get('construct_library_sets', []):
                construct_library_sets = construct_library_sets | set(sample_object.get('construct_library_sets', []))
        if construct_library_sets:
            return sorted(construct_library_sets)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Data Use Limitation Summaries',
            'description': 'The data use limitation summaries of institutional certificates covering the sample associated with this file set which are signed by the same lab (or their partner lab) as the lab that submitted this file set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Data Use Limitation Summary',
                'description': 'A combination of the data use limitation and its modifiers.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def data_use_limitation_summaries(self, request, lab, samples=None):
        summaries_to_return = []
        for sample in samples:
            sample_object = request.embed(
                sample, '@@object_with_select_calculated_properties?field=institutional_certificates')
            for ic in sample_object.get('institutional_certificates', []):
                ic_object = request.embed(
                    ic, '@@object_with_select_calculated_properties?field=data_use_limitation_summary')
                ic_labs = [ic_object.get('lab', None)] + ic_object.get('partner_labs', [])
                if lab in ic_labs:
                    summaries_to_return.append(ic_object.get('data_use_limitation_summary', None))
        if summaries_to_return:
            return sorted(set(summaries_to_return))
        else:
            return ['no certificate']

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Controlled Access',
            'description': 'The controlled access of the institutional certificates covering the sample associated with this file set which are signed by the same lab (or their partner lab) as the lab that submitted this file set.',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def controlled_access(self, request, lab, samples=None):
        controlled_access_to_return = []
        for sample in samples:
            sample_object = request.embed(
                sample, '@@object_with_select_calculated_properties?field=institutional_certificates')
            for ic in sample_object.get('institutional_certificates', []):
                ic_object = request.embed(ic, '@@object?skip_calculated=true')
                ic_labs = [ic_object.get('lab', None)] + ic_object.get('partner_labs', [])
                if lab in ic_labs:
                    controlled_access_to_return.append(ic_object.get('controlled_access'))
        if controlled_access_to_return:
            if any(controlled_access_to_return):
                return True
            else:
                return False


@collection(
    name='analysis-sets',
    unique_key='accession',
    properties={
        'title': 'Analysis Sets',
        'description': 'Listing of analysis sets',
    }
)
class AnalysisSet(FileSet):
    item_type = 'analysis_set'
    schema = load_schema('igvfd:schemas/analysis_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'file_set_type', 'status']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name', 'status']),
        Path('workflows', include=['@id', 'accession', 'name', 'uniform_pipeline', 'status']),
        Path('targeted_genes', include=['@id', 'symbol'])
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, input_file_sets=None, files=None, samples=None, construct_library_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        if files is None:
            files = []
        if samples is None:
            samples = []
        if construct_library_sets is None:
            construct_library_sets = []

        inspected_filesets = set()
        fileset_subclasses = set()
        target_assays = ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq']

        fileset_types = set()
        file_content_types = set()
        targeted_genes = set()
        assay_terms = set()
        cls_derived_assay_titles = set()

        all_assay_summaries = set()
        cls_type_set = set()
        cls_set = set()
        control_type_set = set()
        crispr_modalities = set()
        multiplexing_methods = set()
        crispr_screen_terms = [
            '/assay-terms/OBI_0003659/',
            '/assay-terms/OBI_0003661/'
        ]

        def format_assay(assay_titles, preferred_assay_titles):
            if any(t in target_assays for t in preferred_assay_titles):
                return f"{', '.join(assay_titles)} ({', '.join(preferred_assay_titles)})"
            return ', '.join(preferred_assay_titles or assay_titles)

        if input_file_sets:
            # The file_set_types are included based on the subclass
            # of only the directly associated input_file_sets, not
            # on the subclass of all file sets that are checked.
            for directly_linked_input in input_file_sets:
                fileset_object = request.embed(
                    directly_linked_input,
                    '@@object_with_select_calculated_properties?field=@type'
                )
                fileset_subclasses.add(fileset_object['@type'][0])
            filesets_to_inspect = set(input_file_sets.copy())
            while filesets_to_inspect:
                input_fileset = filesets_to_inspect.pop()
                if input_fileset not in inspected_filesets:
                    inspected_filesets.add(input_fileset)
                    fileset_object = request.embed(
                        input_fileset,
                        '@@object_with_select_calculated_properties?'
                        'field=@type&field=file_set_type&field=measurement_sets'
                        '&field=input_file_sets&field=targeted_genes.symbol'
                        '&field=assay_term&field=applied_to_samples'
                        '&field=assay_titles&field=preferred_assay_titles'
                    )
                    # Trace back from Analysis Sets to identify their
                    # input file sets.
                    if (input_fileset.startswith('/analysis-sets/') and
                            fileset_object.get('input_file_sets', False)):
                        for candidate_fileset in fileset_object.get('input_file_sets'):
                            if candidate_fileset not in inspected_filesets:
                                filesets_to_inspect.add(candidate_fileset)
                    # Retrieve targeted_genes from Measurement Sets.
                    elif input_fileset.startswith('/measurement-sets/'):
                        if 'targeted_genes' in fileset_object:
                            for gene in fileset_object['targeted_genes']:
                                gene_object = request.embed(gene, '@@object?skip_calculated=true')
                                targeted_genes.add(gene_object['symbol'])
                        assay_terms.add(fileset_object['assay_term'])
                        preferred_assay_titles = fileset_object.get('preferred_assay_titles', [])
                        assays_titles = fileset_object.get('assay_titles', [])
                        summary = format_assay(assays_titles, preferred_assay_titles)
                        if summary:
                            all_assay_summaries.add(summary)
                    elif input_fileset.startswith('/auxiliary-sets/'):
                        measurement_sets = fileset_object.get('measurement_sets', [])
                        file_set_type = fileset_object.get('file_set_type')
                        if file_set_type:
                            fileset_types.add(file_set_type)
                        if measurement_sets:
                            for candidate_fileset in measurement_sets:
                                measurement_set_object = request.embed(
                                    candidate_fileset, '@@object?skip_calculated=true')
                                assay_terms.add(measurement_set_object['assay_term'])
                                if candidate_fileset not in inspected_filesets:
                                    filesets_to_inspect.add(candidate_fileset)
                    elif input_fileset.startswith('/construct-library-sets/'):
                        preferred_assay_titles = fileset_object.get('preferred_assay_titles', [])
                        assays_titles = fileset_object.get('assay_titles', [])
                        summary = format_assay(assays_titles, preferred_assay_titles)
                        if summary:
                            cls_derived_assay_titles.add(summary)
                    elif not input_fileset.startswith('/analysis-sets/'):
                        fileset_types.add(fileset_object['file_set_type'])
                    # Collect control types.
                    if 'control_types' in fileset_object:
                        control_type_set = control_type_set | set(fileset_object['control_types'])

        # Collect content_types of files.
        if files:
            for file in files:
                file_object = request.embed(file, '@@object?skip_calculated=true')
                file_content_types.add(file_object['content_type'])

        # Collect construct library set summaries and types
        prop_with_cls = None
        only_cls_input = False
        if construct_library_sets:
            prop_with_cls = construct_library_sets
            only_cls_input = False
        elif fileset_subclasses.issubset({'ConstructLibrarySet', 'CuratedSet'}):
            prop_with_cls = [
                input_file_set for input_file_set in input_file_sets
                if input_file_set.startswith('/construct-library-sets/')
            ]
            only_cls_input = True
        if prop_with_cls:
            for construct_library_set in prop_with_cls:
                construct_library_set_object = request.embed(
                    construct_library_set, '@@object_with_select_calculated_properties?field=summary')
                cls_type_set.add(construct_library_set_object['file_set_type'])
                cls_set.add(construct_library_set_object['summary'])
        cls_phrase = ''
        if len(cls_set) > 0:
            cls_phrase = get_cls_phrase(cls_set, only_cls_input=only_cls_input)

        # Collect CRISPR modalities and file set type from associated samples.
        if samples:
            for sample in samples:
                sample_object = request.embed(sample, '@@object?skip_calculated=true')
                if 'modifications' in sample_object and 'guide library' in cls_type_set:
                    for modification in sample_object['modifications']:
                        modification_object = request.embed(modification, '@@object?skip_calculated=true')
                        crispr_modalities.add(modification_object['modality'])
                if 'multiplexing_methods' in sample_object:
                    for method in sample_object['multiplexing_methods']:
                        multiplexing_methods.add(method)

        # Assay titles if there are input file sets, otherwise unspecified.
        # Only use the CLS derived assay titles if there were no other assay titles.
        if cls_derived_assay_titles and not all_assay_summaries:
            all_assay_summaries = cls_derived_assay_titles
        assay_title_phrase = 'Unspecified assay'
        if all_assay_summaries:
            assay_title_phrase = ', '.join(sorted(all_assay_summaries))
        if 'guide library' in cls_type_set:
            if 'CRISPR' not in assay_title_phrase:
                assay_title_phrase = f'CRISPR {assay_title_phrase}'
        # Add modalities to the assay titles.
        if crispr_modalities:
            if len(crispr_modalities) > 1:
                modality_set = ', '.join(crispr_modalities)
            elif len(crispr_modalities) == 1:
                modality_set = ''.join(crispr_modalities)
            if 'CRISPR' in assay_title_phrase:
                assay_title_phrase = assay_title_phrase.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                assay_title_phrase = f'{modality_set} {assay_title_phrase}'
        if multiplexing_methods:
            method_phrase_map = {
                'barcode based': 'barcode based',
                'genetic': 'genetically'
            }
            mux_method_list = [method_phrase_map[x] for x in sorted(multiplexing_methods)]
            mux_method_phrase = f'({", ".join(mux_method_list)} multiplexed)'
            assay_title_phrase = f'{assay_title_phrase} {mux_method_phrase}'
        # Targeted genes.
        targeted_genes_phrase = ''
        if targeted_genes:
            targeted_genes_phrase = f'targeting {", ".join(targeted_genes)}'
        # The file set types are only shown if the inputs are all Auxiliary Sets
        # and the Measurement Sets related to the Auxiliary Sets are not CRISPR screens.
        file_set_type_phrase = ''
        if fileset_types and len(fileset_subclasses) == 1 and ('AuxiliarySet' in fileset_subclasses):
            if not assay_terms:
                file_set_type_phrase = ', '.join(fileset_types)
            elif not all(x in crispr_screen_terms for x in assay_terms):
                file_set_type_phrase = ', '.join(fileset_types)

        control_phrase = ''
        if len(control_type_set) > 0:
            suffix = ''
            if len(control_type_set) > 1:
                suffix = 's'
            control_types = [control_type for control_type in control_type_set if control_type not in cls_phrase]
            if control_types:
                control_phrase = f'with {", ".join(sorted(control_types))} control{suffix}'

        all_phrases = [
            assay_title_phrase,
            targeted_genes_phrase,
            cls_phrase,
            file_set_type_phrase,
            control_phrase
        ]
        merged_phrase = ' '.join([x for x in all_phrases if x != '']).replace(' : ', ': ')
        if merged_phrase:
            return merged_phrase
        else:
            # Failsafe return value.
            return file_set_type

    @calculated_property(
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'Preferred Assay Title(s) of assays that produced data analyzed in the analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Titles',
                'description': 'Title of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def preferred_assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        preferred_assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=preferred_assay_titles'
            )
            preferred_assay_list.update(
                file_set_object.get(
                    'preferred_assay_titles',
                    []
                )
            )
        return sorted(preferred_assay_list)

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'description': 'Title of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_titles(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        assay_list = set()
        for fileset in input_file_sets:
            file_set_object = request.embed(
                fileset,
                '@@object_with_select_calculated_properties?field=assay_titles&field=@type'
            )
            assay_list.update(
                file_set_object.get(
                    'assay_titles',
                    []
                )
            )
        return sorted(assay_list)

    @calculated_property(
        condition='input_file_sets',
        define=True,
        schema={
            'title': 'Samples',
            'description': 'Samples associated with this analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Sample',
                'description': 'Sample associated with this analysis set.',
                'type': 'string',
                'linkTo': 'Sample'
            },
            'notSubmittable': True,
        }
    )
    def samples(self, request, input_file_sets=None, demultiplexed_samples=None):
        if input_file_sets is not None:
            samples = set()
            for fileset in input_file_sets:
                input_file_set_object = request.embed(fileset, '@@object')
                input_file_set_samples = set(input_file_set_object.get('samples', []))
                if input_file_set_samples:
                    samples = samples | input_file_set_samples
            samples = list(samples)
            if demultiplexed_samples:
                # if the analysis set specifies a demultiplexed sample and all input data is multiplexed return just the demultiplexed_sample
                if not ([sample for sample in samples if not (sample.startswith('/multiplexed-samples/'))]):
                    return demultiplexed_samples
            return sorted(samples)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this analysis set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)

    @calculated_property(
        schema={
            'title': 'Protocols',
            'description': 'Links to the protocol(s) for conducting the assay on Protocols.io.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Protocol',
                'type': 'string',
                'pattern': '^https://www\\.protocols\\.io/(\\S+)$'
            },
            'notSubmittable': True
        }
    )
    def protocols(self, request, input_file_sets=None):
        '''Calculate an array of unique protocols for all measurement sets associated with an analysis set.'''
        protocols = set()
        file_set_objs = []
        if input_file_sets is None:
            input_file_sets = []
        for fileset in input_file_sets:
            file_set_objs.append(
                request.embed(
                    fileset,
                    '@@object_with_select_calculated_properties?field=@type&field=protocols'
                )
            )
        for file_set_obj in file_set_objs:
            if 'MeasurementSet' in file_set_obj.get('@type'):
                protocol = file_set_obj.get('protocols', [])
                protocols.update(protocol)
        return sorted(protocols)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Simplified Sample Summary',
            'description': 'A summary of the samples associated with input file sets of this analysis set.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def sample_summary(self, request, samples=None):
        taxa = set()
        sample_classification_term_target = dict()
        treatment_purposes = set()
        treatment_summaries = set()
        differentiation_times = set()
        construct_library_set_types = set()
        modification_summaries = set()
        sorted_from = set()
        targeted_genes_for_sorting = set()
        cellular_sub_pools = set()

        treatment_purpose_to_adjective = {
            'activation': 'activated',
            'agonist': 'agonized',
            'antagonist': 'antagonized',
            'control': 'treated with a control',
            'differentiation': 'differentiated',
            'de-differentiation': 'de-differentiated',
            'perturbation': 'perturbed',
            'selection': 'selected',
            'stimulation': 'stimulated'
        }

        two_classification_cases = {
            'differentiated cell specimen, pooled cell specimen': ['pooled differentiated cell specimen'],
            'pooled cell specimen, reprogrammed cell specimen': ['pooled reprogrammed cell specimen'],
            'cell line, pooled cell specimen': ['pooled cell specimen']
        }

        classification_to_prefix = {
            'differentiated cell specimen': 'differentiated',
            'reprogrammed cell specimen': 'reprogrammed',
            'pooled differentiated cell specimen': 'pooled differentiated',
            'pooled reprogrammed cell specimen': 'pooled reprogrammed'
        }

        for sample in samples:
            sample_object = request.embed(sample, '@@object')

            taxa.add(sample_object.get('taxa', ''))

            # Group sample and targeted sample terms according to classification.
            # Other metadata such as treatment info are lumped together.
            mux_prefix = ''
            sample_classifications = sorted(sample_object['classifications'])
            if 'multiplexed sample' in sample_object['classifications']:
                sample_classifications.remove('multiplexed sample')
                mux_prefix = 'multiplexed sample of '
            if ', '.join(sorted(sample_classifications)) in two_classification_cases:
                sample_classifications = two_classification_cases[', '.join(sorted(sample_classifications))]
            # The variable "classification" can potentially be very long for
            # a Multiplexed Sample, but it will be entirely dropped for
            # Multiplexed Sample in the end - so it is ok.
            classification = f"{mux_prefix}{' and '.join(sample_classifications)}"
            if classification not in sample_classification_term_target:
                sample_classification_term_target[classification] = set()

            for term in sample_object['sample_terms']:
                sample_term_object = request.embed(term, '@@object?skip_calculated=true')
                sample_phrase = f"{sample_term_object['term_name']}"
                # Avoid redundancy of classification and term name
                # e.g. "HFF-1 cell cell line"
                if not classification.startswith('multiplexed sample of'):
                    if sample_phrase.endswith('cell') and 'cell' in classification:
                        sample_phrase = sample_phrase.replace('cell', classification)
                    elif sample_phrase.endswith(' gastruloid') and 'gastruloid' in classification:
                        sample_phrase = sample_phrase.replace(' gastruloid', '')
                    elif 'cell' in sample_phrase and classification in classification_to_prefix:
                        sample_phrase = f'{classification_to_prefix[classification]} {sample_phrase}'

                targeted_sample_suffix = ''
                if 'targeted_sample_term' in sample_object:
                    targeted_sample_term_object = request.embed(
                        sample_object['targeted_sample_term'], '@@object?skip_calculated=true')
                    targeted_sample_suffix = f"induced to {targeted_sample_term_object['term_name']}"
                if targeted_sample_suffix:
                    sample_phrase = f'{sample_phrase} {targeted_sample_suffix}'
                sample_classification_term_target[classification].add(sample_phrase)

            if 'time_post_change' in sample_object:
                time = sample_object['time_post_change']
                time_unit = sample_object['time_post_change_units']
                differentiation_times.add(f'{time} {time_unit}')
            if 'modifications' in sample_object:
                for modification in sample_object['modifications']:
                    modification_object = request.embed(
                        modification, '@@object_with_select_calculated_properties?field=summary')
                    modification_summaries.add(modification_object['summary'])
            if 'construct_library_sets' in sample_object:
                for construct_library_set in sample_object['construct_library_sets']:
                    cls_object = request.embed(construct_library_set, '@@object?skip_calculated=true')
                    construct_library_set_types.add(cls_object['file_set_type'])
            if 'sorted_from' in sample_object:
                sorted_from.add(True)
                for file_set in sample_object['file_sets']:
                    if file_set.startswith('/measurement-sets/'):
                        fileset_object = request.embed(file_set, '@@object?skip_calculated=true')
                        if 'targeted_genes' in fileset_object:
                            for gene in fileset_object['targeted_genes']:
                                gene_object = request.embed(gene, '@@object?skip_calculated=true')
                                targeted_genes_for_sorting.add(gene_object['symbol'])
            if 'treatments' in sample_object:
                for treatment in sample_object['treatments']:
                    treatment_object = request.embed(
                        treatment, '@@object_with_select_calculated_properties?field=summary')
                    treatment_purposes.add(treatment_purpose_to_adjective.get(treatment_object['purpose'], ''))
                    truncated_summary = treatment_object['summary'].split(' of ')[1]
                    treatment_summaries.add(truncated_summary)
            if 'cellular_sub_pool' in sample_object:
                cellular_sub_pools.add(sample_object['cellular_sub_pool'])

        all_sample_terms = []
        for classification in sorted(sample_classification_term_target.keys()):
            terms_by_classification = f"{', '.join(sorted(sample_classification_term_target[classification]))}"
            # Put the terms after the "multiplexed sample of" and drop
            # the underlying classifications
            if 'multiplexed sample of' in classification:
                terms_by_classification = f'multiplexed sample of {terms_by_classification}'
            # Differentiated, reprogrammed, pooled cell specimen can be merged
            # into the terms_by_classification before this. Therefore we don't
            # want to append it to the terms_by_classification a second time.
            elif not any(x in terms_by_classification for x in [
                    'differentiated cell specimen', 'reprogrammed cell specimen', 'pooled cell specimen', 'primary cell']
            ):
                # Insert the classification before the targeted_sample_term if it exists.
                if 'induced to' in terms_by_classification:
                    terms_by_classification = terms_by_classification.replace(
                        'induced to', f'{classification} induced to'
                    )
                else:
                    terms_by_classification = f'{terms_by_classification} {classification}'
            elif any(x in terms_by_classification for x in [
                    'differentiated cell specimen', 'reprogrammed cell specimen', 'pooled cell specimen', 'primary cell']
            ):
                # Don't add anything when the classification was already in
                # the terms_by_classification.
                terms_by_classification = f'{terms_by_classification}'
            # Failsafe case.
            else:
                terms_by_classification = f'{terms_by_classification} {classification}'

            all_sample_terms.append(terms_by_classification)

        differentiation_time_phrase = ''
        if differentiation_times:
            differentiation_time_phrase = f'at {", ".join(sorted(differentiation_times))}(s) post change'
        treatments_phrase = ''
        if treatment_purposes and treatment_summaries:
            treatments_phrase = f"{', '.join(sorted(treatment_purposes))} with {', '.join(sorted(treatment_summaries))}"
        modification_summary_phrase = ''
        if modification_summaries:
            modification_summaries = sorted(modification_summaries)
            modification_summary_phrase = f'modified with {", ".join(modification_summaries)}'
        construct_library_set_type_phrase = ''
        if construct_library_set_types:
            construct_library_set_type_phrase = f'transfected with a {", ".join(construct_library_set_types)}'
        sorted_phrase = ''
        if sorted_from:
            if targeted_genes_for_sorting:
                sorted_phrase = f'sorted on expression of {", ".join(targeted_genes_for_sorting)}'
            else:
                sorted_phrase = f'sorted into bins'
        cellular_sub_pool_phrase = ''
        if cellular_sub_pools:
            cellular_sub_pool_phrase = f'cellular sub pool(s): {", ".join(sorted(cellular_sub_pools))}'

        taxa_phrase = f'{", ".join([x for x in taxa if x != ""])}'
        additional_phrases = [
            differentiation_time_phrase,
            treatments_phrase,
            modification_summary_phrase,
            construct_library_set_type_phrase,
            sorted_phrase,
            cellular_sub_pool_phrase
        ]
        additional_phrases_joined = ', '.join([x for x in additional_phrases if x != ''])
        additional_phrase_suffix = ''
        if additional_phrases_joined:
            additional_phrase_suffix = f', {additional_phrases_joined}'
        summary = f"{taxa_phrase} {', '.join(all_sample_terms)}{additional_phrase_suffix}".strip()

        return summary

    @calculated_property(
        schema={
            'title': 'Functional Assay Mechanisms',
            'description': 'The biological processes measured by the functional assays.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Phenotype Term',
                'type': 'string',
                'linkTo': 'PhenotypeTerm'
            },
            'notSubmittable': True
        }
    )
    def functional_assay_mechanisms(self, request, input_file_sets=None):
        mechanism_objects = []
        file_set_objs = []
        if input_file_sets is None:
            input_file_sets = []
        for fileset in input_file_sets:
            file_set_objs.append(
                request.embed(
                    fileset,
                    '@@object_with_select_calculated_properties?field=@type&field=functional_assay_mechanisms'
                )
            )
        for file_set_object in file_set_objs:
            if 'MeasurementSet' in file_set_object.get('@type') or 'AnalysisSet' in file_set_object.get('@type'):
                mechanism_objects.extend(file_set_object.get('functional_assay_mechanisms', []))
        return sorted(set(mechanism_objects))

    @calculated_property(
        schema={
            'title': 'Workflows',
            'description': 'A workflow for computational analysis of genomic data. A workflow is made up of analysis steps.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Workflow',
                'type': 'string',
                'linkTo': 'Workflow'
            }
        }
    )
    def workflows(self, request, files=None):
        analysis_set_workflows_set = set()
        # Get a list of file objects
        file_objs = get_file_objs_from_files(request, files)
        for file_obj in file_objs:
            analysis_step_version = file_obj.get('analysis_step_version')
            if analysis_step_version:
                # Get analysis step version and request the object
                analysis_step_version_obj = request.embed(analysis_step_version, '@@object?skip_calculated=true')
                # Get analysis step and request the object
                analysis_step = analysis_step_version_obj.get('analysis_step')
                if analysis_step:
                    analysis_step_obj = request.embed(analysis_step, '@@object?skip_calculated=true')
                    # Get workflow and add to the set
                    workflow = analysis_step_obj.get('workflow')
                    if workflow:
                        analysis_set_workflows_set.add(workflow)
        return sorted(analysis_set_workflows_set)

    @calculated_property(
        condition='input_file_sets',
        schema={
            'title': 'Targeted Genes',
            'description': 'A list of genes targeted by the input measurement sets assays.',
            'type': 'array',
            'notSubmittable': True,
            'uniqueItem': True,
            'minItems': 1,
            'items': {
                'title': 'Targeted Gene',
                'type': 'string',
                'linkTo': 'Gene'
            }
        }
    )
    def targeted_genes(self, request, input_file_sets=None):
        if input_file_sets is None:
            input_file_sets = []
        analysis_set_targeted_genes = set()
        for input_file_set in input_file_sets:
            if input_file_set.startswith('/measurement-sets/') or input_file_set.startswith('/analysis-sets/'):
                input_file_set_object = request.embed(
                    input_file_set, '@@object_with_select_calculated_properties?field=targeted_genes')
                if 'targeted_genes' in input_file_set_object:
                    analysis_set_targeted_genes.update(input_file_set_object['targeted_genes'])
        return sorted(analysis_set_targeted_genes)


@collection(
    name='curated-sets',
    unique_key='accession',
    properties={
        'title': 'Curated Sets',
        'description': 'Listing of curated sets',
    }
)
class CuratedSet(FileSet):
    item_type = 'curated_set'
    schema = load_schema('igvfd:schemas/curated_set.json')
    embedded_with_frame = FileSet.embedded_with_frame
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        define=True,
        schema={
            'title': 'Assemblies',
            'description': 'The genome assemblies to which the referencing files in the file set are utilizing (e.g., GRCh38).',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assembly',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assemblies(self, request, files=None):
        if files:
            assembly_values = set()
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('assembly'):
                    assembly_values.add(file_object.get('assembly'))
            if assembly_values:
                return sorted(assembly_values)

    @calculated_property(
        define=True,
        schema={
            'title': 'Transcriptome Annotations',
            'description': 'The annotation versions of the reference resource.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Transcriptome Annotation',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def transcriptome_annotations(self, request, files=None):
        if files:
            annotation_values = set()
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('transcriptome_annotation'):
                    annotation_values.add(file_object.get('transcriptome_annotation'))
            if annotation_values:
                return sorted(annotation_values)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, file_set_type, assemblies=None, transcriptome_annotations=None, taxa=None):
        summary_message = ''
        if taxa:
            summary_message += f'{taxa} '
        if assemblies:
            assembly_values_joined = ' '.join(assemblies)
            summary_message += f'{assembly_values_joined} '
        if transcriptome_annotations:
            annotation_values_joined = ' '.join(transcriptome_annotations)
            summary_message += f'{annotation_values_joined} '
        summary_message += file_set_type
        return summary_message


@collection(
    name='measurement-sets',
    unique_key='accession',
    properties={
        'title': 'Measurement Sets',
        'description': 'Listing of measurement sets',
    })
class MeasurementSet(FileSet):
    item_type = 'measurement_set'
    schema = load_schema('igvfd:schemas/measurement_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('assay_term', include=['@id', 'term_name', 'assay_slims', 'status']),
        Path('control_file_sets', include=['@id', 'accession', 'aliases', 'status']),
        Path('related_multiome_datasets', include=['@id', 'accession', 'status']),
        Path('auxiliary_sets', include=['@id', 'accession', 'aliases', 'file_set_type', 'status']),
        Path('construct_library_sets.small_scale_gene_list', include=[
             '@id', 'small_scale_gene_list', 'summary', 'geneid', 'symbol', 'name', 'status']),
        Path('files.sequencing_platform', include=['@id', 'term_name', 'status']),
        Path('targeted_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name', 'status'])
    ]

    audit_inherit = FileSet.audit_inherit + [
        'auxiliary_sets',
        'assay_term'
    ]

    set_status_up = FileSet.set_status_up + [
        'assay_term',
        'auxiliary_sets'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'items': {
                'type': 'string'
            },
            'notSubmittable': True
        }
    )
    def assay_titles(self, request, assay_term):
        if assay_term:
            assay_term_obj = request.embed(assay_term, '@@object?skip_calculated=true')
            term_name = assay_term_obj.get('term_name')
            if term_name:
                return [term_name]

    @calculated_property(
        condition='multiome_size',
        schema={
            'title': 'Related Multiome Datasets',
            'description': 'Related datasets included in the multiome experiment this measurement set is a part of.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Related Multiome Dataset',
                'description': 'Related dataset included in the multiome experiment this measurement set is a part of.',
                'type': 'string',
                'linkTo': 'MeasurementSet'
            },
            'notSubmittable': True,
        }
    )
    def related_multiome_datasets(self, request, samples=None):
        object_id = self.jsonld_id(request)
        if samples:
            related_datasets = []
            for sample in samples:
                sample_object = request.embed(sample, '@@object')
                if sample_object.get('file_sets'):
                    for file_set_id in sample_object.get('file_sets'):
                        if '/measurement-sets/' == file_set_id[:18] and \
                            object_id != file_set_id and \
                                file_set_id not in related_datasets:
                            related_datasets.append(file_set_id)
            return sorted(related_datasets)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, assay_term, assay_titles, preferred_assay_titles=None, samples=None, control_types=None, targeted_genes=None, construct_library_sets=None):
        if construct_library_sets is None:
            construct_library_sets = []
        modality_set = set()
        cls_set = set()
        cls_type_set = set()
        multiplexing_methods = set()
        control_phrase = ''
        cls_phrase = ''
        modality_phrase = ''
        assay_phrase = ''
        target_phrase = ''

        if construct_library_sets:
            for construct_library_set in construct_library_sets:
                construct_library_set_object = request.embed(
                    construct_library_set, '@@object_with_select_calculated_properties?field=summary')
                cls_type_set.add(construct_library_set_object['file_set_type'])
                cls_set.add(construct_library_set_object['summary'])

        for sample in samples:
            sample_object = request.embed(sample, '@@object')
            if sample_object.get('modifications') and 'guide library' in cls_type_set:
                for modification in sample_object.get('modifications'):
                    modality = request.embed(modification).get('modality', '')
                    if modality:
                        modality_set.add(modality)
            if 'multiplexing_methods' in sample_object:
                for method in sample_object['multiplexing_methods']:
                    multiplexing_methods.add(method)

        assay = assay_titles[0] if assay_titles else None
        preferred_assay_title = preferred_assay_titles[0]
        if preferred_assay_title in ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq']:
            assay = f'{assay} ({preferred_assay_title})'
        else:
            assay = preferred_assay_title

        if targeted_genes:
            # Special case for CRISPR screens using flow cytometry
            if request.embed(assay_term)['term_id'] == 'OBI:0003661':
                target_phrase = f' sorted on the expression of'
            else:
                target_phrase = f' targeting'
            if len(targeted_genes) > 5:
                target_phrase = f'{target_phrase} {len(targeted_genes)} genes'
            elif len(targeted_genes) <= 5:
                genes = []
                for targeted_gene in targeted_genes:
                    gene_object = request.embed(targeted_gene, '@@object?skip_calculated=true')
                    gene_name = (gene_object.get('symbol'))
                    genes.append(gene_name)
                genes = sorted(genes)
                target_phrase = f'{target_phrase} {", ".join(genes)}'

        if 'guide library' in cls_type_set:
            if 'CRISPR' not in assay:
                assay = f'CRISPR {assay}'

        if len(modality_set) > 1:
            modality_set = ', '.join(modality_set)
            if 'CRISPR' in assay:
                assay_phrase = assay.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                modality_phrase = f'{modality_set} '
                assay_phrase = f'{assay}'
            assay_phrase = f' {assay}'
        if len(modality_set) == 1:
            modality_set = ''.join(modality_set)
            if 'CRISPR' in assay:
                assay_phrase = assay.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                modality_phrase = f'{modality_set} '
                assay_phrase = f'{assay}'
        if len(modality_set) == 0:
            assay_phrase = f'{assay}'
        if multiplexing_methods:
            method_phrase_map = {
                'barcode based': 'barcode based',
                'genetic': 'genetically'
            }
            mux_method_list = [method_phrase_map[x] for x in sorted(multiplexing_methods)]
            mux_method_phrase = f'({", ".join(mux_method_list)} multiplexed)'
            assay_phrase = f'{assay_phrase} {mux_method_phrase}'

        if len(cls_set) > 0:
            cls_phrase = f' {get_cls_phrase(cls_set)}'

        if control_types:
            non_redundant_control_types = [control_type for control_type in sorted(
                control_types) if control_type not in cls_phrase]
            if non_redundant_control_types:
                control_phrase = f'{", ".join(non_redundant_control_types)} '
        # Special case for Y2H assays if control_type is not specified.
        if request.embed(assay_term)['term_id'] == 'OBI:0000288' and control_types is None:
            control_phrase = 'post-selection '

        sentence = ''
        sentence_parts = [
            control_phrase,
            modality_phrase,
            assay_phrase,
            target_phrase,
            cls_phrase,
        ]
        for phrase in sentence_parts:
            if phrase != '':
                sentence += phrase
        return sentence

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this measurement set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this measurement set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)

    @calculated_property(
        schema={
            'title': 'Externally Hosted',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def externally_hosted(self, request, files=None):
        externally_hosted_value = False
        if files:
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('externally_hosted'):
                    externally_hosted_value = True
        return externally_hosted_value


@collection(
    name='model-sets',
    unique_key='accession',
    properties={
        'title': 'Model Sets',
        'description': 'Listing of model sets',
    }
)
class ModelSet(FileSet):
    item_type = 'model_set'
    schema = load_schema('igvfd:schemas/model_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'status']),
        Path('assessed_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('software_versions.software', include=['@id', 'summary', 'title', 'source_url', 'download_id', 'status'])
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + [
        'software_versions'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, model_name, model_version, prediction_objects, assessed_genes=None):
        # Get assessed genes phrase
        assessed_gene_phrase = get_assessed_gene_phrase(request, assessed_genes)
        return ' '.join(filter(None, [
            model_name,
            model_version,
            file_set_type,
            f'for {assessed_gene_phrase}' if assessed_genes else '',
            'predicting',
            ', '.join(prediction_objects)
        ]))

    @calculated_property(
        schema={
            'title': 'Externally Hosted',
            'type': 'boolean',
            'notSubmittable': True,
        }
    )
    def externally_hosted(self, request, files=None):
        externally_hosted_value = False
        if files:
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                if file_object.get('externally_hosted'):
                    externally_hosted_value = True
        return externally_hosted_value

    @calculated_property(
        schema={
            'title': 'Software Versions',
            'description': 'The software versions used to produce this predictive model.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Software Version',
                'description': 'A software version used to produce this predictive model.',
                'type': 'string',
                'linkTo': 'SoftwareVersion',
            },
            'notSubmittable': True

        }
    )
    def software_versions(self, request, files=None):
        software_versions = []
        if files:
            for file in files:
                if file.startswith('/model-files/'):
                    file_object = request.embed(file, '@@object?skip_calculated=true')
                    analysis_step_version = file_object.get('analysis_step_version', '')
                    if analysis_step_version:
                        analysis_step_version_object = request.embed(
                            analysis_step_version, '@@object?skip_calculated=true')
                        software_versions = software_versions + \
                            analysis_step_version_object.get('software_versions', [])
        if software_versions:
            return sorted(set(software_versions))


@collection(
    name='auxiliary-sets',
    unique_key='accession',
    properties={
        'title': 'Auxiliary Sets',
        'description': 'Listing of auxiliary sets',
    })
class AuxiliarySet(FileSet):
    item_type = 'auxiliary_set'
    schema = load_schema('igvfd:schemas/auxiliary_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('measurement_sets', include=['@id', 'accession', 'aliases', 'preferred_assay_titles', 'status']),
    ]
    audit_inherit = FileSet.audit_inherit
    rev = FileSet.rev | {'measurement_sets': ('MeasurementSet', 'auxiliary_sets')}
    set_status_up = FileSet.set_status_up + [

    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Measurement Sets',
        'description': 'The measurement sets that link to this auxiliary set.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Measurement Set',
            'type': 'string',
            'linkFrom': 'MeasurementSet.auxiliary_sets',
        },
        'notSubmittable': True
    })
    def measurement_sets(self, request, measurement_sets):
        return paths_filtered_by_status(request, measurement_sets)

    @calculated_property(
        condition='measurement_sets',
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'The preferred assay titles of the measurement sets that used this auxiliary set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Title',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def preferred_assay_titles(self, request, measurement_sets=None):
        if measurement_sets is None:
            measurement_sets = []
        preferred_assay_titles = set()
        for measurement_set in measurement_sets:
            preferred_assays = request.embed(
                measurement_set, '@@object?skip_calculated=true').get('preferred_assay_titles', [])
            if preferred_assays:
                preferred_assay_titles.update(preferred_assays)
        return sorted(preferred_assay_titles)

    @calculated_property(
        condition='measurement_sets',
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_titles(self, request, measurement_sets=None):
        if measurement_sets is None:
            measurement_sets = []
        assay_titles = set()
        for measurement_set in measurement_sets:
            assays = request.embed(
                measurement_set, '@@object_with_select_calculated_properties?field=assay_titles').get('assay_titles', [])
            if assays:
                assay_titles.update(assays)
        return sorted(assay_titles)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, measurement_sets=None):
        if not measurement_sets:
            return f'{file_set_type}'
        measurement_sets_summaries = sorted(set(
            [request.embed(measurement_set, '@@object_with_select_calculated_properties?field=summary').get('summary') for measurement_set in measurement_sets if measurement_set]))
        return f'{file_set_type} for {", ".join(measurement_sets_summaries)}'

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this auxiliary set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Donor',
                'description': 'Donor of a sample associated with this auxiliary set.',
                'type': 'string',
                'linkTo': 'Donor'
            },
            'notSubmittable': True,
        }
    )
    def donors(self, request, samples=None):
        return get_donors_from_samples(request, samples)


@collection(
    name='prediction-sets',
    unique_key='accession',
    properties={
        'title': 'Prediction Sets',
        'description': 'Listing of prediction sets',
    })
class PredictionSet(FileSet):
    item_type = 'prediction_set'
    schema = load_schema('igvfd:schemas/prediction_set.json')
    embedded_with_frame = FileSet.embedded_with_frame + [
        Path('samples.construct_library_sets', include=['@id', 'accession', 'summary', 'status']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('assessed_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name', 'status']),
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the prediction set.',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, assessed_genes=None, scope=None, files=None):
        # Get scope info
        scope_phrase = ''
        if scope:
            scope_phrase = f' on scope of {scope}'
        software_versions = set()
        if files is not None:
            for file in files:
                file_object = request.embed(file, '@@object?skip_calculated=true')
                if 'analysis_step_version' in file_object:
                    asv_object = request.embed(
                        file_object['analysis_step_version'],
                        '@@object?skip_calculated=true')
                    for software_version in asv_object['software_versions']:
                        software_version_object = request.embed(
                            software_version,
                            '@@object_with_select_calculated_properties?field=summary')
                        software_versions.add(software_version_object['summary'])
        software_version_phrase = None
        if software_versions:
            software_version_phrase = f'using {", ".join(sorted(software_versions))}'
        # Get assessed genes info
        assessed_genes_phrase = get_assessed_gene_phrase(request, assessed_genes)
        # Final summary
        return ' '.join(filter(None, [
            file_set_type,
            f'prediction{scope_phrase}',
            f'for {assessed_genes_phrase}' if assessed_genes else '',
            software_version_phrase
        ]))


@collection(
    name='construct-library-sets',
    unique_key='accession',
    properties={
        'title': 'Construct Library Sets',
        'description': 'Listing of construct library sets',
    })
class ConstructLibrarySet(FileSet):
    item_type = 'construct_library_set'
    schema = load_schema('igvfd:schemas/construct_library_set.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases',
             'content_type', 'href', 'file_format', 'upload_status', 'status']),
        Path('integrated_content_files', include=['@id', 'accession',
             'aliases', 'content_type', 'file_format', 'upload_status', 'status']),
        Path('control_for', include=['@id', 'accession', 'aliases', 'status']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name', 'status']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms', 'status']),
        Path('applied_to_samples', include=['@id', '@type', 'accession',
             'aliases', 'classifications', 'disease_terms', 'donors', 'sample_terms', 'targeted_sample_term', 'status', 'summary', 'modifications', 'treatments', 'nucleic_acid_delivery']),
        Path('applied_to_samples.donors', include=['@id', 'taxa', 'status']),
        Path('applied_to_samples.disease_terms', include=['@id', 'term_name', 'status']),
        Path('applied_to_samples.sample_terms', include=['@id', 'term_name', 'status']),
        Path('applied_to_samples.targeted_sample_term', include=['@id', 'term_name', 'status']),
        Path('applied_to_samples.modifications', include=['@id', 'modality', 'summary', 'status']),
        Path('applied_to_samples.treatments', include=['@id', 'treatment_term_name', 'summary', 'status']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases', 'status']),
        Path('orf_list', include=['@id', 'orf_id', 'genes', 'aliases', 'status']),
        Path('orf_list.genes', include=['@id', 'symbol', 'status']),
        Path('publications', include=['@id', 'publication_identifiers', 'status']),
    ]
    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
        'integrated_content_files'
    ]

    rev = FileSet.rev | {'applied_to_samples': ('Sample', 'construct_library_sets')}

    set_status_up = FileSet.set_status_up + ['integrated_content_files']
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Applied to Samples',
        'description': 'The samples that link to this construct library set.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Applied to Sample',
            'type': 'string',
            'linkFrom': 'Sample.construct_library_sets',
        },
        'notSubmittable': True
    })
    def applied_to_samples(self, request, applied_to_samples):
        return paths_filtered_by_status(request, applied_to_samples)

    @calculated_property(
        define=True,
        schema={
            'title': 'File Sets',
            'description': 'The file sets that used this construct library set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'File Set',
                'type': 'string',
                'linkTo': 'FileSet'
            },
            'notSubmittable': True
        })
    def file_sets(self, request, applied_to_samples=None):
        if applied_to_samples is None:
            applied_to_samples = []
        linked_file_sets = set()
        for sample in applied_to_samples:
            sample_object = request.embed(sample, '@@object_with_select_calculated_properties?field=file_sets')
            for file_set in sample_object.get('file_sets', []):
                linked_file_sets.add(file_set)
        if linked_file_sets:
            return sorted(linked_file_sets)

    @calculated_property(
        condition='file_sets',
        define=True,
        schema={
            'title': 'Preferred Assay Titles',
            'description': 'The preferred assay titles of the file sets that used this construct library set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Preferred Assay Title',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def preferred_assay_titles(self, request, file_sets=None):
        if file_sets is None:
            file_sets = []
        preferred_assay_titles = set()
        for file_set in file_sets:
            if file_set.startswith('/measurement-sets/'):
                preferred_assays = request.embed(
                    file_set, '@@object?skip_calculated=true').get('preferred_assay_titles', [])
                if preferred_assays:
                    preferred_assay_titles.update(preferred_assays)
        return sorted(preferred_assay_titles)

    @calculated_property(
        condition='file_sets',
        define=True,
        schema={
            'title': 'Assay Term Names',
            'description': 'Ontology term names from Ontology of Biomedical Investigations (OBI) for assays.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Term Names',
                'type': 'string'
            },
            'notSubmittable': True
        })
    def assay_titles(self, request, file_sets=None):
        if file_sets is None:
            file_sets = []
        assay_titles = set()
        for file_set in file_sets:
            if file_set.startswith('/measurement-sets/'):
                assays = request.embed(
                    file_set, '@@object_with_select_calculated_properties?field=assay_titles').get('assay_titles', [])
                if assays:
                    assay_titles.update(assays)
        return sorted(assay_titles)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, scope, selection_criteria, small_scale_gene_list=None, large_scale_gene_list=None, guide_type=None,
                small_scale_loci_list=None, large_scale_loci_list=None, exon=None, tile=None, orf_list=None, associated_phenotypes=None,
                control_types=None, targeton=None, preferred_assay_titles=None, integrated_content_files=None):
        if preferred_assay_titles is None:
            preferred_assay_titles = []
        if integrated_content_files is None:
            integrated_content_files = []
        library_type = file_set_type
        target_phrase = ''
        pheno_terms = []
        pheno_phrase = ''
        preposition = ''
        pool_phrase = ''
        criteria = []
        criteria = criteria + selection_criteria

        if library_type == 'guide library':
            if guide_type == 'sgRNA':
                library_type = 'guide (sgRNA) library'
            if guide_type == 'pgRNA':
                library_type = 'guide (pgRNA) library'

        if scope == 'control':
            return f'{", ".join(sorted(control_types))} {library_type}'
        if scope == 'loci':
            if small_scale_loci_list and len(small_scale_loci_list) > 1:
                target_phrase = f' {len(small_scale_loci_list)} genomic loci'
            elif large_scale_loci_list:
                target_phrase = f' many genomic loci'
            else:
                target_phrase = f' a genomic locus'
        if scope == 'genes':
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' {len(small_scale_gene_list)} genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                target_phrase = f' {gene_name}'
            elif large_scale_gene_list:
                target_phrase = f' many genes'
        if scope == 'exon':
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' exon {exon} of multiple genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                target_phrase = f' exon {exon} of {gene_name}'
        if scope == 'interactors':
            if orf_list and len(orf_list) > 1:
                target_phrase = f' {len(orf_list)} open reading frames'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                orf_object = request.embed(orf_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                orf_id = (orf_object.get('orf_id'))
                target_phrase = f' open reading frame {orf_id} of {gene_name}'
        if scope == 'tile':
            tile_id = tile['tile_id']
            start = tile['tile_start']
            end = tile['tile_end']
            if small_scale_gene_list and len(small_scale_gene_list) > 1:
                target_phrase = f' tile {tile_id} of multiple genes'
            elif small_scale_gene_list and len(small_scale_gene_list) == 1:
                gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
                gene_name = (gene_object.get('symbol'))
                target_phrase = f' tile {tile_id} of {gene_name} (AA {start}-{end})'
        if scope == 'genome-wide':
            target_phrase = ' genome-wide'
        if scope == 'targeton':
            gene_object = request.embed(small_scale_gene_list[0], '@@object?skip_calculated=true')
            gene_name = gene_object.get('symbol', '')
            target_phrase = f' {targeton} of {gene_name}'

        if associated_phenotypes:
            for pheno in associated_phenotypes:
                pheno_object = request.embed(pheno, '@@object?skip_calculated=true')
                term_name = (pheno_object.get('term_name'))
                pheno_terms.append(term_name)
            if len(pheno_terms) in [1, 2]:
                phenos = ' and '.join(pheno_terms)
                pheno_phrase = f' associated with {phenos}'
            else:
                pheno_phrase = f' associated with {len(pheno_terms)} phenotypes'

        if preferred_assay_titles and 'STARR-seq' in preferred_assay_titles:
            thousand_genomes_ids = set()
            for integrated_content_file in integrated_content_files:
                integrated_content_file_object = request.embed(integrated_content_file, '@@object?skip_calculated=true')
                file_set_object = request.embed(
                    integrated_content_file_object['file_set'], '@@object_with_select_calculated_properties?field=donors')
                donors = file_set_object.get('donors', [])
                for donor in donors:
                    donor_object = request.embed(donor, '@@object?skip_calculated=true')
                    dbxrefs = donor_object.get('dbxrefs', [])
                    for dbxref in dbxrefs:
                        if dbxref.startswith('IGSR'):
                            thousand_genomes_id = dbxref.split(':')[1]
                            thousand_genomes_ids.add(thousand_genomes_id)
            if thousand_genomes_ids:
                thousand_genomes_ids = ', '.join(sorted(thousand_genomes_ids))
                pool_phrase = f' pooled from 1000 Genomes donors: {thousand_genomes_ids}'

        if file_set_type == 'expression vector library':
            if 'genes' in criteria:
                criteria.remove('genes')
            selections = ', '.join(criteria)
            if selections:
                selections = f' ({selections})'
            preposition = ' of'
            return f'{library_type}{preposition}{target_phrase}{selections}{pheno_phrase}'
        else:
            selections = ', '.join(criteria)
            if scope == 'genome-wide':
                preposition = ''
            else:
                preposition = ' in'
            return f'{library_type} targeting {selections}{preposition}{target_phrase}{pheno_phrase}{pool_phrase}'
