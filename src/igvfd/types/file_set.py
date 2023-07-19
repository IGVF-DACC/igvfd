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
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases']),
        Path('control_for', include=['@id', 'accession', 'aliases']),
        Path('donors', include=['@id', 'taxa']),
        Path('samples', include=['@id', 'accession', 'aliases',
             'biosample_term', 'technical_sample_term', 'summary', 'donors']),
        Path('samples.donors', include=['@id', 'accession', 'aliases'])
    ]

    @calculated_property(schema={
        'title': 'Files',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'File.file_set',
        },
        'notSubmittable': True
    })
    def files(self, request, files):
        return paths_filtered_by_status(request, files)

    @calculated_property(schema={
        'title': 'File sets controlled by this file set',
        'type': 'array',
        'items': {
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.control_file_sets',
        },
        'notSubmittable': True
    })
    def control_for(self, request, control_for):
        return paths_filtered_by_status(request, control_for)


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
    embedded_with_frame = FileSet.embedded_with_frame

    @calculated_property(
        schema={
            'title': 'Assay Title',
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
    def assay_title(self, request, input_file_sets=None):
        assay_title = set()
        if input_file_sets is not None:
            for fileset in input_file_sets:
                file_set_object = request.embed(fileset, '@@object')
                if file_set_object.get('assay_title') and \
                        'MeasurementSet' in file_set_object.get('@type'):
                    assay_title.add(file_set_object.get('assay_title'))
            return list(assay_title)


@collection(
    name='curated-sets',
    unique_key='accession',
    properties={
        'title': 'Curated Set',
        'description': 'Listing of curated sets',
    }
)
class CuratedSet(FileSet):
    item_type = 'curated_set'
    schema = load_schema('igvfd:schemas/curated_set.json')
    embedded_with_frame = FileSet.embedded_with_frame


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
        Path('related_multiome_datasets', include=['@id', 'accession'])
    ]

    audit_inherit = [
        'related_multiome_datasets'
    ]

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


@collection(
    name='construct-libraries',
    unique_key='accession',
    properties={
        'title': 'Construct Library',
        'description': 'Listing of construct libraries',
    })
class ConstructLibrary(FileSet):
    item_type = 'construct_library'
    schema = load_schema('igvfd:schemas/construct_library.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('files', include=['@id', 'accession', 'aliases']),
        Path('control_for', include=['@id', 'accession', 'aliases'])
    ]


@collection(
    name='models',
    unique_key='accession',
    properties={
        'title': 'Model',
        'description': 'Listing of models',
    }
)
class Model(FileSet):
    item_type = 'model'
    schema = load_schema('igvfd:schemas/model.json')
    embedded_with_frame = FileSet.embedded_with_frame


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
    embedded_with_frame = FileSet.embedded_with_frame


@collection(
    name='predictions',
    unique_key='accession',
    properties={
        'title': 'Prediction',
        'description': 'Listing of predictions',
    })
class Prediction(FileSet):
    item_type = 'prediction'
    schema = load_schema('igvfd:schemas/prediction.json')
    embedded_with_frame = FileSet.embedded_with_frame
