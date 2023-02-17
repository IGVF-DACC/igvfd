from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path

from .base import (
    Item
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
    embedded_with_frame = [
        Path('award', include=['@id', 'component', 'name']),
        Path('lab', include=['@id', 'title']),
        Path(
            'donors',
            include=[
                '@id',
                'accession',
                'taxa',
                'uuid'
            ]
        ),
    ]

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
    embedded_with_frame = [
        Path('award', include=['@id', 'component', 'name']),
        Path('lab', include=['@id', 'title']),
    ]


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
    embedded_with_frame = [
        Path('assay_term', include=['@id', 'term_name']),
        Path('award', include=['@id', 'component', 'name']),
        Path('donors', include=['@id', 'accession', 'taxa']),
        Path('lab', include=['@id', 'title']),
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
