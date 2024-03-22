from snovault import (
    collection,
    load_schema,
)
from .base import (
    Item
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
