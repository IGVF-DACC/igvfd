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


def inspect_fileset(request, fileset, inspected_filesets, assay_terms, fileset_types):
    if fileset not in inspected_filesets:
        inspected_filesets.add(fileset)
        fileset_object = request.embed(fileset, '@@object?skip_calculated=true')
        if fileset.startswith('/measurement-sets/'):
            if 'preferred_assay_title' in fileset_object:
                assay_terms.add(fileset_object['preferred_assay_title'])
            else:
                assay_terms.add(request.embed(fileset_object['assay_term'],
                                '@@object?skip_calculated=true')['term_name'])
        elif not fileset.startswith('/analysis-sets/'):
            fileset_types.add(fileset_object['file_set_type'])
        elif (fileset.startswith('/analysis-sets/') and
              fileset_object.get('input_file_sets', False)):
            for input_fileset in fileset_object.get('input_file_sets'):
                if input_fileset.startswith('/analysis-sets/'):
                    properties = {'analysis': input_fileset}
                    path = Path('analysis', include=['input_file_sets'])
                    path.expand(request, properties)
                    if (properties['analysis'] != {}):
                        pruned_sets = (set(properties['analysis']['input_file_sets']) - inspected_filesets)
                        for pruned_fileset in pruned_sets:
                            inspect_fileset(request, pruned_fileset, inspected_filesets, assay_terms, fileset_types)
                    else:
                        inspect_fileset(request, input_fileset, inspected_filesets, assay_terms, fileset_types)
                else:
                    inspect_fileset(request, input_fileset, inspected_filesets, assay_terms, fileset_types)


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
        'control_for': ('FileSet', 'control_file_sets')
    }
    embedded_with_frame = [
        Path('award.contact_pi', include=['@id', 'contact_pi', 'component', 'title']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases', 'content_type',
             'file_format', 'file_size', 'href', 's3_uri', 'submitted_file_name',
                               'creation_timestamp']),
        Path('control_for', include=['@id', 'accession', 'aliases']),
        Path('donors', include=['@id', 'accession', 'aliases', 'taxa']),
        Path('samples.sample_terms', include=[
            '@id',
            'accession',
            'aliases',
            'treatments',
            'cell_fate_change_treatments',
            'classification',
            'construct_library_sets',
            'disease_terms',
            'modifications',
            'sample_terms',
            'summary',
            'targeted_sample_term',
            'taxa',
            'term_name',
        ]),
        Path('samples.targeted_sample_term', include=['@id', 'term_name']),
    ]

    audit_inherit = [
        'award',
        'lab',
        'files',
        'documents',
        'control_file_sets',
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
        'description': 'The timestamp the first file object in the file_set was created.',
        'comment': 'Do not submit. The timestamp is automatically calculated.',
        'type': 'string',
        'format': 'date-time',
        'notSubmittable': True
    })
    def submitted_files_timestamp(self, request, files):
        if files:
            timestamps = set()
            for current_file_path in files:
                file_object = request.embed(current_file_path, '@@object?skip_calculated=true')
                timestamp = file_object.get('creation_timestamp', None)
                if timestamp:
                    timestamps.add(timestamp)
            res = sorted(timestamps, key=lambda x: datetime.strptime(x, '%Y-%m-%dT%H:%M:%S.%f%z'))
            return res[0]


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
        Path('input_file_sets', include=['@id', 'accession', 'aliases', 'file_set_type'])
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
        filesets_to_inspect = set()
        inspected_filesets = set()
        assay_terms = set()
        fileset_types = set()
        if input_file_sets:
            filesets_to_inspect = input_file_sets
            while filesets_to_inspect:
                input_fileset = filesets_to_inspect.pop()
                if input_fileset not in inspected_filesets:
                    inspected_filesets.add(input_fileset)
                    fileset_object = request.embed(input_fileset, '@@object?skip_calculated=true')
                    if input_fileset.startswith('/measurement-sets/'):
                        if 'preferred_assay_title' in fileset_object:
                            assay_terms.add(fileset_object['preferred_assay_title'])
                        else:
                            assay_terms.add(request.embed(fileset_object['assay_term'],
                                            '@@object?skip_calculated=true')['term_name'])
                    elif not input_fileset.startswith('/analysis-sets/'):
                        fileset_types.add(fileset_object['file_set_type'])
                    elif (input_fileset.startswith('/analysis-sets/') and
                          fileset_object.get('input_file_sets', False)):
                        filesets_to_inspect.append(fileset_object.get('input_file_sets'))
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
        assay_title = set()
        if input_file_sets is not None:
            for fileset in input_file_sets:
                file_set_object = request.embed(fileset, '@@object')
                if file_set_object.get('preferred_assay_title') and \
                        'MeasurementSet' in file_set_object.get('@type'):
                    assay_title.add(file_set_object.get('preferred_assay_title'))
                elif 'MeasurementSet' in file_set_object.get('@type'):
                    assay = request.embed(file_set_object['assay_term'], '@@object')
                    assay_title.add(assay.get('term_name'))
            return list(assay_title)

    @calculated_property(
        condition='samples',
        schema={
            'title': 'Donors',
            'description': 'The donors of the samples associated with this analysis set.',
            'type': 'array',
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
        Path('readout', include=['@id', 'term_name']),
        Path('library_construction_platform', include=['@id', 'term_name']),
        Path('control_file_sets', include=['@id', 'accession', 'aliases']),
        Path('related_multiome_datasets', include=['@id', 'accession']),
        Path('auxiliary_sets', include=['@id', 'accession', 'aliases']),
        Path('samples.treatments', include=['@id', 'purpose', 'treatment_type', 'summary']),
        Path('samples.cell_fate_change_treatments', include=['@id', 'purpose', 'treatment_type', 'summary']),
        Path('samples.disease_terms', include=['@id', 'term_name']),
        Path('samples.modifications', include=['@id', 'modality']),
        Path('samples.construct_library_sets', include=['@id', 'accession', 'summary']),
    ]

    audit_inherit = FileSet.audit_inherit + [
        'auxiliary_sets',
        'library_construction_platform',
        'assay_term',
        'readout',
    ]

    set_status_up = FileSet.set_status_up + [
        'assay_term',
        'library_construction_platform',
        'readout'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(
        condition='multiome_size',
        schema={
            'title': 'Related Multiome Datasets',
            'description': 'Related datasets included in the multiome experiment this measurement set is a part of.',
            'type': 'array',
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
    def summary(self, request, assay_term, preferred_assay_title=None, readout=None,
                samples=None):
        assay = request.embed(assay_term)['term_name']
        modality_set = set()
        cls_set = set()
        cls_phrase = ''
        modality_phrase = ''
        assay_phrase = ''
        readout_phrase = ''
        preferred_title_phrase = ''

        if samples:
            for sample in samples:
                sample_object = request.embed(sample, '@@object')
                if sample_object.get('modifications'):
                    for modification in sample_object.get('modifications'):
                        modality = request.embed(modification)['modality']
                        modality_set.add(modality)
                if sample_object.get('construct_library_sets'):
                    for construct_library in sample_object.get('construct_library_sets'):
                        cls_summary = request.embed(construct_library)['summary']
                        cls_set.add(cls_summary)
        if readout:
            readout_term = request.embed(readout)['term_name']
            readout_phrase = f' followed by {readout_term}'
        if preferred_assay_title:
            preferred_title_phrase = f' ({preferred_assay_title})'
        if len(modality_set) > 1:
            modality_phrase = f'mixed'
            assay_phrase = f' {assay}'
        if len(modality_set) == 1:
            modality_set = ''.join(modality_set)
            if assay == 'CRISPR screen':
                assay_phrase = f'CRISPR {modality_set} screen'
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
            preferred_title_phrase,
            cls_phrase,
            readout_phrase
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
        Path('measurement_sets', include=['@id', 'accession', 'aliases']),
    ]
    audit_inherit = FileSet.audit_inherit
    rev = FileSet.rev | {'measurement_sets': ('MeasurementSet', 'auxiliary_sets')}
    set_status_up = FileSet.set_status_up + [
        'library_construction_platform'
    ]
    set_status_down = FileSet.set_status_down + []

    @calculated_property(schema={
        'title': 'Measurement Sets',
        'description': 'The measurement sets that link to this auxiliary set.',
        'type': 'array',
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
    ]
    audit_inherit = FileSet.audit_inherit
    set_status_up = FileSet.set_status_up + []
    set_status_down = FileSet.set_status_down + []


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
        Path('files', include=['@id', 'accession', 'aliases', 'content_type', 'file_format']),
        Path('control_for', include=['@id', 'accession', 'aliases']),
        Path('associated_phenotypes', include=['@id', 'term_id', 'term_name']),
        Path('small_scale_gene_list', include=['@id', 'geneid', 'symbol', 'name', 'synonyms']),
        Path('applied_to_samples', include=['@id', 'accession', 'aliases']),
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
                small_scale_loci_list=None, large_scale_loci_list=None, exon=None, tile=None, associated_phenotypes=None):
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
                phenos = ', '.join(pheno_terms)
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
