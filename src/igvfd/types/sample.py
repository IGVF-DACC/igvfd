from snovault import (
    abstract_collection,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@abstract_collection(
    name='samples',
    unique_key='accession',
    properties={
        'title': 'Samples',
        'description': 'Listing of samples',
    })
class Sample(Item):
    base_types = ['Sample'] + Item.base_types
    schema = load_schema('igvfd:schemas/sample.json')


@abstract_collection(
    name='biosamples',
    unique_key='accession',
    properties={
        'title': 'Biosamples',
        'description': 'Listing of biosamples',
    })
class Biosample(Sample):
    base_types = ['Biosample'] + Sample.base_types
    schema = load_schema('igvfd:schemas/biosample.json')


@collection(
    name='cell-lines',
    unique_key='accession',
    properties={
        'title': 'Cell lines',
        'description': 'Listing of cell lines',
    })
class CellLine(Biosample):
    item_type = 'cell_line'
    schema = load_schema('igvfd:schemas/cell_line.json')
