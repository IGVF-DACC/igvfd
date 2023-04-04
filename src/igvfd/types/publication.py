from snovault import (
    collection,
    load_schema,
    calculated_property
)

from .base import (
    Item,
    datetime
)


@collection(
    name='publications',
    unique_key='publication:identifier',
    properties={
        'title': 'Publications',
        'description': 'Listing of publications',
    }
)
class Publication(Item):
    item_type = 'publication'
    schema = load_schema('igvfd:schemas/publication.json')

    def unique_keys(self, properties):
        keys = super(Publication, self).unique_keys(properties)
        if properties.get('identifiers'):
            keys.setdefault('alias', []).extend(properties['identifiers'])
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
