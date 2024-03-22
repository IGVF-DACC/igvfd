from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    Item,
    paths_filtered_by_status
)
from snovault.util import Path


@collection(
    name='open-reading-frame',
    unique_key='open_reading_frame:orf_id',
    properties={
        'title': 'Open Reading Frame',
        'description': 'Protein-encoding open reading frames (ORF)',
    }
)
class OpenReadingFrame(Item):
    item_type = 'open_reading_frame'
    schema = load_schema('igvfd:schemas/open_reading_frame.json')
    name_key = 'orf_id'
    embedded_with_frame = [
        Path('gene', include=['@id', 'symbol']),
    ]
    rev = {
        'gene_symbol': ('Gene', 'symbol')
    }

    @calculated_property(schema={
        'title': 'Gene Symbol',
        'description': 'Gene symbol approved by the official nomenclature.',
        'type': 'array',
        'uniqueItems': True,
        'minItems': 1,
        'items': {
            'title': 'Gene Symbol',
            'type': ['array', 'object'],
            'linkFrom': 'Gene.symbol',
        },
        'notSubmittable': True
    })
    def gene_symbol(self, request, gene_symbol):
        return paths_filtered_by_status(request, gene_symbol)
