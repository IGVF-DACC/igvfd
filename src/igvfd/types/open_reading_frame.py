from snovault import (
    collection,
    load_schema,
    calculated_property
)
from .base import (
    Item
)
from snovault.util import Path


@collection(
    name='open-reading-frames',
    unique_key='open_reading_frame:orf_id',
    properties={
        'title': 'Open Reading Frames',
        'description': 'Protein-encoding open reading frames (ORF)',
    }
)
class OpenReadingFrame(Item):
    item_type = 'open_reading_frame'
    schema = load_schema('igvfd:schemas/open_reading_frame.json')
    name_key = 'orf_id'
    embedded_with_frame = [
        Path('genes', include=['@id', 'symbol', 'geneid', 'status']),
    ]

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, request, orf_id, genes, protein_id=None):
        protein_phrase = ''
        if protein_id:
            protein_phrase = f' - {protein_id}'
        gene_symbols = []
        for gene_item in genes:
            gene_object = request.embed(gene_item)
            gene_symbols.append(gene_object['symbol'])
        return f'{orf_id} of {", ".join(gene_symbols)}{protein_phrase}'
