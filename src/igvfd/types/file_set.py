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
    return list(set(donor_objects))


def get_fileset_objs_from_input_file_sets(request, input_file_sets):
    '''Get file set objects from an array of input file sets'''
    file_set_objs = []
    if input_file_sets is not None:
        for fileset in input_file_sets:
            file_set_objs.append(request.embed(fileset, '@@object'))
    return file_set_objs


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
        'input_file_set_for': ('FileSet', 'input_file_sets')
    }
    embedded_with_frame = [
        Path('award.contact_pi', include=['@id', 'contact_pi', 'component', 'title']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases', 'content_type',
             'file_format', 'file_size', 'href', 's3_uri', 'submitted_file_name',
                               'creation_timestamp', 'sequencing_platform', 'upload_status']),
        Path('control_for', include=['@id', 'accession', 'aliases']),
        Path('donors', include=['@id', 'accession', 'aliases', 'sex', 'status', 'taxa']),
        Path('samples.sample_terms', include=[
            '@id',
            '@type',
            'accession',
            'aliases',
            'treatments',
            'cell_fate_change_treatments',
            'classifications',
            'construct_library_sets',
            'disease_terms',
            'modifications',
            'sample_terms',
            'status',
            'summary',
            'targeted_sample_term',
            'taxa',
            'term_name',
        ]),
        Path('samples.disease_terms', include=['@id', 'term_name']),
        Path('samples.targeted_sample_term', include=['@id', 'term_name']),
        Path('publications', include=['@id', 'publication_identifiers']),
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
            'type': ['string', 'object'],
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
            'type': ['string', 'object'],
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
    def submitted_files_timestamp(self, request, files, auxiliary_sets=[]):
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
        'title': 'Input File Set For',
        'description': 'The file sets that use this file set as an input.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Input File Set For',
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.input_file_sets',
        },
        'notSubmittable': True
    })
    def input_file_set_for(self, request, input_file_set_for):
        return paths_filtered_by_status(request, input_file_set_for)


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
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'file_set_type']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name'])
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
    def summary(self, request, file_set_type, input_file_sets=[]):
        sentence = f'{file_set_type}'
        inspected_filesets = set()
        assay_terms = set()
        fileset_types = set()
        if input_file_sets:
            filesets_to_inspect = set(input_file_sets.copy())

            while filesets_to_inspect:
                input_fileset = filesets_to_inspect.pop()
                if input_fileset not in inspected_filesets:
                    inspected_filesets.add(input_fileset)
                    fileset_object = request.embed(input_fileset, '@@object?skip_calculated=true')
                    if input_fileset.startswith('/measurement-sets/'):
                        assay_terms.add(fileset_object.get('preferred_assay_title', ''))
                    elif not input_fileset.startswith('/analysis-sets/'):
                        fileset_types.add(fileset_object['file_set_type'])
                    elif (input_fileset.startswith('/analysis-sets/') and
                          fileset_object.get('input_file_sets', False)):
                        for candidate_fileset in fileset_object.get('input_file_sets'):
                            if candidate_fileset not in inspected_filesets:
                                filesets_to_inspect.add(candidate_fileset)
        if assay_terms:
            terms = ', '.join(sorted(assay_terms))
            sentence += f' of {terms} data'
        elif fileset_types:
            terms = ', '.join(sorted(fileset_types))
            sentence += f' of {terms} data'
        else:
            sentence += f' of data'
        return sentence

    @calculated_property(
        schema={
            'title': 'Assay Titles',
            'description': 'Title(s) of assays that produced data analyzed in the analysis set.',
            'type': 'array',
            'minItems': 1,
            'uniqueItems': True,
            'items': {
                'title': 'Assay Title',
                'description': 'Title of assay that produced data analyzed in the analysis set.',
                'type': 'string'
            },
            'notSubmittable': True,
        }
    )
    def assay_titles(self, request, input_file_sets=None):
        assay_titles = set()
        if input_file_sets is not None:
            for fileset in input_file_sets:
                file_set_object = request.embed(fileset, '@@object')
                if 'MeasurementSet' in file_set_object.get('@type'):
                    preferred_assay_title = file_set_object.get('preferred_assay_title')
                    if preferred_assay_title:
                        assay_titles.add(preferred_assay_title)
                elif 'AnalysisSet' in file_set_object.get('@type'):
                    input_analysis_assay_titles = set(file_set_object.get('assay_titles', []))
                    if input_analysis_assay_titles:
                        assay_titles = assay_titles | input_analysis_assay_titles
                elif 'AuxiliarySet' in file_set_object.get('@type'):
                    for measurement_set in file_set_object.get('measurement_sets'):
                        measurement_set_object = request.embed(measurement_set, '@@object')
                        preferred_assay_title = measurement_set_object.get('preferred_assay_title')
                        if preferred_assay_title:
                            assay_titles.add(preferred_assay_title)
            return list(assay_titles)

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
        file_set_objs = get_fileset_objs_from_input_file_sets(request=request, input_file_sets=input_file_sets)
        for file_set_obj in file_set_objs:
            if 'MeasurementSet' in file_set_obj.get('@type'):
                protocol = file_set_obj.get('protocols', [])
                if protocol:
                    protocols.update(protocol)
        return list(protocols)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Sample Summary',
            'description': 'A summary of the samples associated with input file sets of this analysis set.',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def sample_summary(self, request, samples=None):
        sample_classification_term_target = dict()
        treatment_purposes = set()
        differentiation_times = set()
        construct_library_set_types = set()
        sorted_from = set()
        targeted_genes_for_sorting = set()

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

        for sample in samples:
            sample_object = request.embed(sample, '@@object')

            # Group sample and targeted sample terms according to classification.
            # Other metadata such as treatment info are lumped together.
            classification = ' and '.join(sample_object['classifications'])
            if classification not in sample_classification_term_target:
                sample_classification_term_target[classification] = set()

            for term in sample_object['sample_terms']:
                sample_term_object = request.embed(term, '@@object?skip_calculated=true')
                if 'targeted_sample_term' in sample_object:
                    targeted_sample_term_object = request.embed(
                        sample_object['targeted_sample_term'], '@@object?skip_calculated=true')
                    sample_classification_term_target[classification].add(
                        f"{sample_term_object['term_name']} "
                        f"induced to {targeted_sample_term_object['term_name']}"
                    )
                else:
                    sample_classification_term_target[classification].add(
                        f"{sample_term_object['term_name']}"
                    )

            if 'time_post_change' in sample_object:
                time = sample_object['time_post_change']
                time_unit = sample_object['time_post_change_units']
                differentiation_times.add(f'{time} {time_unit}')
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
                    treatment_object = request.embed(treatment, '@@object?skip_calculated=true')
                    treatment_purposes.add(treatment_purpose_to_adjective.get(treatment_object['purpose'], ''))

        all_sample_terms = []
        for classification in sorted(sample_classification_term_target.keys()):
            terms_by_classification = f"{', '.join(sample_classification_term_target[classification])}"
            # Insert the classification before the targeted_sample_term if it exists.
            if 'induced to' in terms_by_classification:
                terms_by_classification = terms_by_classification.replace(
                    'induced to', f'{classification} induced to'
                )
            else:
                terms_by_classification = f'{terms_by_classification} {classification}'
            all_sample_terms.append(terms_by_classification)

        differentiation_time_phrase = ''
        if differentiation_times:
            differentiation_time_phrase = f'at {len(differentiation_times)} time point(s) post change'
        treatments_phrase = ''
        if treatment_purposes:
            treatments_phrase = f"{', '.join(treatment_purposes)} with treatment(s)"
        construct_library_set_type_phrase = ''
        if construct_library_set_types:
            construct_library_set_type_phrase = f'modified with a {", ".join(construct_library_set_types)}'
        sorted_phrase = ''
        if sorted_from:
            if targeted_genes_for_sorting:
                sorted_phrase = f'sorted on expression of {", ".join(targeted_genes_for_sorting)}'
            else:
                sorted_phrase = f'sorted into bins'

        additional_phrases = [
            differentiation_time_phrase,
            treatments_phrase,
            construct_library_set_type_phrase,
            sorted_phrase
        ]
        additional_phrases_joined = ', '.join([x for x in additional_phrases if x != ''])
        additional_phrase_suffix = ''
        if additional_phrases_joined:
            additional_phrase_suffix = f', {additional_phrases_joined}'
        summary = f"{', '.join(all_sample_terms)}{additional_phrase_suffix}"

        return summary
    
    @calculated_property(
        schema={
            'title': 'Functional Assay Mechanisms',
            'description': 'The biological mechanism(s) the functional assay measures.',
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
        '''Calculate an array of unique biological mechanism(s) measured by the funcional assays associated with an analysis set.'''
        mechanism_objs = []
        file_set_objs = get_fileset_objs_from_input_file_sets(request=request, input_file_sets=input_file_sets)
        for file_set_object in file_set_objs:
            if 'MeasurementSet' in file_set_object.get('@type') or 'AnalysisSet' in file_set_object.get('@type'):
                mechanism_objs.extend(file_set_object.get('functional_assay_mechanisms', []))
        return list(set(mechanism_objs))


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
                return sorted(list(assembly_values))

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
                return sorted(list(annotation_values))

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
        Path('assay_term', include=['@id', 'term_name']),
        Path('control_file_sets', include=['@id', 'accession', 'aliases']),
        Path('related_multiome_datasets', include=['@id', 'accession']),
        Path('auxiliary_sets', include=['@id', 'accession', 'aliases', 'file_set_type']),
        Path('samples.treatments', include=['@id', 'purpose', 'treatment_type', 'summary']),
        Path('samples.cell_fate_change_treatments', include=['@id', 'purpose', 'treatment_type', 'summary']),
        Path('samples.disease_terms', include=['@id', 'term_name']),
        Path('samples.modifications', include=['@id', 'modality']),
        Path('samples.construct_library_sets.small_scale_gene_list', include=[
             '@id', 'file_set_type', 'accession', 'small_scale_gene_list', 'summary', 'geneid', 'symbol', 'name']),
        Path('files.sequencing_platform', include=['@id', 'term_name']),
        Path('targeted_genes', include=['@id', 'geneid', 'symbol', 'name', 'synonyms']),
        Path('functional_assay_mechanisms', include=['@id', 'term_id', 'term_name'])
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
            return related_datasets

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, assay_term, preferred_assay_title=None, samples=None):
        assay = request.embed(assay_term)['term_name']
        modality_set = set()
        cls_set = set()
        cls_phrase = ''
        modality_phrase = ''
        assay_phrase = ''

        for sample in samples:
            sample_object = request.embed(sample, '@@object')
            if sample_object.get('modifications'):
                for modification in sample_object.get('modifications'):
                    modality = request.embed(modification).get('modality', '')
                    if modality:
                        modality_set.add(modality)
            if sample_object.get('construct_library_sets'):
                for construct_library in sample_object.get('construct_library_sets'):
                    cls_summary = request.embed(construct_library)['summary']
                    cls_set.add(cls_summary)

        if preferred_assay_title in ['10x multiome', '10x multiome with MULTI-seq', 'SHARE-seq']:
            assay = f'{assay} ({preferred_assay_title})'
        else:
            assay = preferred_assay_title

        if len(modality_set) > 1:
            modality_phrase = f'mixed'
            assay_phrase = f' {assay}'
        if len(modality_set) == 1:
            modality_set = ''.join(modality_set)
            if 'CRISPR' in assay:
                assay_phrase = assay.replace('CRISPR', f'CRISPR {modality_set}')
            else:
                modality_phrase = ''
                assay_phrase = f'{assay}'
        if len(modality_set) == 0:
            assay_phrase = f'{assay}'

        if len(cls_set) > 0:
            cls_phrases = []
            for summary in cls_set:
                article = 'a'
                if any(summary.startswith(x) for x in ['a', 'e', 'i', 'o', 'u']):
                    article = 'an'
                cls_phrases.append(f'{article} {summary[0].lower()}{summary[1:]}')
            if len(cls_phrases) == 1:
                cls_phrase = cls_phrases[0]
            elif len(cls_phrases) == 2:
                cls_phrase = ' and '.join(cls_phrases)
            elif len(cls_phrases) > 2:
                cls_phrase = ', '.join(cls_phrases[:-1]) + ', and ' + cls_phrases[-1]
            cls_phrase = f' integrating {cls_phrase}'

        sentence = ''
        sentence_parts = [
            modality_phrase,
            assay_phrase,
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
        Path('input_file_sets', include=['@id', 'accession', 'aliases'])
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + [
        'software_version'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, model_name, model_version, prediction_objects):
        return f'{model_name} {model_version} {file_set_type} predicting {", ".join(prediction_objects)}'


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
        Path('measurement_sets', include=['@id', 'accession', 'aliases', 'preferred_assay_title']),
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
            'type': ['string', 'object'],
            'linkFrom': 'MeasurementSet.auxiliary_sets',
        },
        'notSubmittable': True
    })
    def measurement_sets(self, request, measurement_sets):
        return paths_filtered_by_status(request, measurement_sets)

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
        measurement_sets_summaries = [request.embed(measurement_set, '@@object').get('summary')
                                      for measurement_set in measurement_sets[:2] if measurement_set]
        if len(measurement_sets) > 2:
            remainder = f'... and {len(measurement_sets) - 2} more measurement set{"s" if len(measurement_sets) - 2 != 1 else ""}'
            measurement_sets_summaries = measurement_sets_summaries + [remainder]
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
        Path('samples.construct_library_sets', include=['@id', 'accession', 'summary']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms']),
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
    def summary(self, file_set_type, scope=None):
        scope_phrase = ''
        if scope:
            scope_phrase = f' on scope of {scope}'
        return f'{file_set_type} prediction{scope_phrase}'


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
        Path('files', include=['@id', 'accession', 'aliases', 'content_type', 'file_format', 'upload_status']),
        Path('integrated_content_files', include=['@id', 'accession',
             'aliases', 'content_type', 'file_format', 'upload_status']),
        Path('control_for', include=['@id', 'accession', 'aliases']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms']),
        Path('applied_to_samples', include=['@id', '@type', 'accession',
             'aliases', 'classifications', 'disease_terms', 'donors', 'sample_terms', 'targeted_sample_term', 'status', 'summary']),
        Path('applied_to_samples.donors', include=['@id', 'taxa']),
        Path('applied_to_samples.disease_terms', include=['@id', 'term_name']),
        Path('applied_to_samples.sample_terms', include=['@id', 'term_name']),
        Path('applied_to_samples.targeted_sample_term', include=['@id', 'term_name']),
        Path('large_scale_gene_list', include=['@id', 'accession', 'aliases']),
        Path('large_scale_loci_list', include=['@id', 'accession', 'aliases']),
        Path('orf_list', include=['@id', 'orf_id', 'genes', 'aliases']),
        Path('orf_list.genes', include=['@id', 'symbol']),
        Path('publications', include=['@id', 'publication_identifiers']),
    ]
    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
    ]

    rev = FileSet.rev | {'applied_to_samples': ('Sample', 'construct_library_sets')}

    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Applied to Samples',
        'description': 'The samples that link to this construct library set.',
        'type': 'array',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Applied to Sample',
            'type': ['string', 'object'],
            'linkFrom': 'Sample.construct_library_sets',
        },
        'notSubmittable': True
    })
    def applied_to_samples(self, request, applied_to_samples):
        return paths_filtered_by_status(request, applied_to_samples)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, file_set_type, scope, selection_criteria, small_scale_gene_list=None, large_scale_gene_list=None, guide_type=None,
                small_scale_loci_list=None, large_scale_loci_list=None, exon=None, tile=None, orf_list=None, associated_phenotypes=None):
        library_type = ''
        target_phrase = ''
        pheno_terms = []
        pheno_phrase = ''
        preposition = ''
        criteria = []
        criteria = criteria + selection_criteria

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

        if file_set_type == 'expression vector library':
            library_type = 'Expression vector library'
        if file_set_type == 'guide library':
            if guide_type == 'sgRNA':
                library_type = 'Guide (sgRNA) library'
            if guide_type == 'pgRNA':
                library_type = 'Guide (pgRNA) library'
        if file_set_type == 'reporter library':
            library_type = 'Reporter library'

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
            return f'{library_type} targeting {selections}{preposition}{target_phrase}{pheno_phrase}'
