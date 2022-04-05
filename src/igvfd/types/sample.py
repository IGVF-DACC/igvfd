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


@collection(
    name='biosamples',
    unique_key='accession',
    properties={
        'title': 'Biosamples',
        'description': 'Listing of biosamples',
    })
class Biosample(Sample):
    item_type = 'biosample'
    schema = load_schema('igvfd:schemas/biosample.json')


@collection(
    name='technical_samples',
    unique_key='accession',
    properties={
        'title': 'Technical Samples',
        'description': 'Listing of technical samples',
    })
class TechnicalSample(Sample):
    item_type = 'technical_sample'
    schema = load_schema('igvfd:schemas/technical_sample.json')
