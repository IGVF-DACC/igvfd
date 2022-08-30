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
    name='files',
    unique_key='accession',
    properties={
        'title': 'Files',
        'description': 'Listing of files',
    })
class File(Item):
    item_type = 'file'
    base_types = ['File'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/file.json')


@collection(
    name='sequence-data',
    unique_key='accession',
    properties={
        'title': 'Sequence data',
        'description': 'Listing of sequence data files',
    })
class SequenceData(File):
    item_type = 'sequence_data'
    schema = load_schema('igvfd:schemas/sequence_data.json')
