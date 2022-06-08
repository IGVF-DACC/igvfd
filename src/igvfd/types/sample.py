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
    name='samples',
    unique_key='accession',
    properties={
        'title': 'Samples',
        'description': 'Listing of samples',
    })
class Sample(Item):
    item_type = 'sample'
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
    item_type = 'biosample'
    base_types = ['Biosample'] + Sample.base_types
    schema = load_schema('igvfd:schemas/biosample.json')

    @calculated_property(
        schema={
            'title': 'Sex',
            'type': 'string',
        }
    )
    def sex(self, donor=None):
        if donor and donor.get('sex'):
            return donor.get('sex')


@collection(
    name='primary-cells',
    unique_key='accession',
    properties={
        'title': 'Primary cells',
        'description': 'Listing of primary cells',
    })
class PrimaryCell(Biosample):
    item_type = 'primary_cell'
    schema = load_schema('igvfd:schemas/primary_cell.json')


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


@collection(
    name='tissues',
    unique_key='accession',
    properties={
        'title': 'Tissues',
        'description': 'Listing of tissues',
    })
class Tissue(Biosample):
    item_type = 'tissue'
    schema = load_schema('igvfd:schemas/tissue.json')


@collection(
    name='differentiated-tissues',
    unique_key='accession',
    properties={
        'title': 'Differentiated tissues',
        'description': 'Listing of differentiated tissues',
    })
class DifferentiatedTissue(Biosample):
    item_type = 'differentiated_tissue'
    schema = load_schema('igvfd:schemas/differentiated_tissue.json')


@collection(
    name='differentiated-cells',
    unique_key='accession',
    properties={
        'title': 'Differentiated cells',
        'description': 'Listing of differentiated cells',
    })
class DifferentiatedCell(Biosample):
    item_type = 'differentiated_cell'
    schema = load_schema('igvfd:schemas/differentiated_cell.json')


@collection(
    name='technical-samples',
    unique_key='accession',
    properties={
        'title': 'Technical Samples',
        'description': 'Listing of technical samples',
    })
class TechnicalSample(Sample):
    item_type = 'technical_sample'
    schema = load_schema('igvfd:schemas/technical_sample.json')
