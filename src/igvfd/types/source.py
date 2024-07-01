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

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the source.',
            'notSubmittable': True,
        }
    )
    def summary(self, title):
        return title
