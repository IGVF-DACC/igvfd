from snovault import (
    collection,
    load_schema
)
from .base import (
    Item
)
from snovault.util import Path


@collection(
    name='sources',
    unique_key='source:name',
    properties={
        'title': 'Sources',
        'description': 'Listing of external sources',
    }
)
class Source(Item):
    item_type = 'source'
    schema = load_schema('igvfd:schemas/source.json')
    name_key = 'name'
    embedded_with_frame = [
        Path('submitted_by', include=['@id', 'title']),
    ]
