from snovault import (
    collection,
    load_schema,
)
from .base import (
    Item
)
from snovault.util import Path


@collection(
    name='open-reading-frames',
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

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(OpenReadingFrame, self).unique_keys(properties)
        keys.setdefault('open_reading_frame:orf_id',
                        []).append(properties['orf_id'])
        return keys
