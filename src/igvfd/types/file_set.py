from snovault import (
    abstract_collection,
    calculated_property,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@abstract_collection(
    name='file-sets',
    unique_key='accession',
    properties={
        'title': 'File sets',
        'description': 'Listing of file sets',
    })
class FileSet(Item):
    item_type = 'file_set'
    base_types = ['FileSet'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file_set.json')


@collection(
    name='analysis-sets',
    unique_key='accession',
    properties={
        'title': 'Analysis sets',
        'description': 'Listing of analysis sets',
    })
class AnalysisSet(FileSet):
    item_type = 'analysis_set'
    schema = load_schema('igvfd:schemas/analysis_set.json')

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
    def assay_title(self, request, input_file_set=None):
        assay_titles = []
        if input_file_set is not None:
            for fileset in input_file_set:
                file_set_object = request.embed(fileset, '@@object')
                if file_set_object.get('assay_title'):
                    assay_title.append(file_set_object.get('assay_title'))
            return list(set(assay_title))
