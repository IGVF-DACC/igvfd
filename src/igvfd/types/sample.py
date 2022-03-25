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
        'description': 'Listing samples',
    })
class Sample(Item):
    base_types = ['Sample'] + Item.base_types
    schema = load_schema('igvfd:schemas/sample.json')


@collection(
    name='biosamples',
    unique_key='accession',
    properties={
        'title': 'Biosamples',
        'description': 'Listing biosamples',
    })
class Biosample(Sample):
    item_type = 'biosample'
    schema = load_schema('igvfd:schemas/biosample.json')
