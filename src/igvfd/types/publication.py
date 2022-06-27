from snovault import (
    collection,
    load_schema,
    calculated_property
)

from .base import (
    Item,
)


@collection(
    name='publications',
    unique_key='publication:identifier',
    properties={
        'title': 'Publications',
        'description': 'Publication pages',
    })
class Publication(Item):
    item_type = 'publication'
    schema = load_schema('igvfd:schemas/publication.json')

    def unique_keys(self, properties):
        keys = super(Publication, self).unique_keys(properties)
        if properties.get('identifiers'):
            keys.setdefault('alias', []).extend(properties['identifiers'])
        return keys

    @calculated_property(condition='date_published', schema={
        'title': 'Publication year',
        'type': 'integer',
    })
    def publication_year(self, date_published):
        likely_year = date_published[:4]
        if likely_year.isdigit():
            return int(date_published[:4])
        else:
            return None
