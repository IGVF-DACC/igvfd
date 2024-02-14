from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item,
    datetime
)


@collection(
    name='publications',
    unique_key='publication:publication_identifiers',
    properties={
        'title': 'Publications',
        'description': 'Listing of publications',
    }
)
class Publication(Item):
    item_type = 'publication'
    schema = load_schema('igvfd:schemas/publication.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(Publication, self).unique_keys(properties)
        if properties.get('publication_identifiers'):
            keys.setdefault('alias', []).extend(properties['publication_identifiers'])
        return keys

    @calculated_property(
        condition='date_published',
        schema={
            'title': 'Publication Year',
            'type': 'integer',
            'notSubmittable': True,
        }
    )
    def publication_year(self, date_published):
        year = datetime.strptime(date_published, '%Y-%m-%d').year
        return year
