from snovault import (
    collection,
    load_schema,
    calculated_property,
)
from snovault.util import Path
from .base import (
    Item,
    datetime,
    paths_filtered_by_status
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

    rev = {
        'samples': ('Sample', 'publications'),
        'donors': ('Donor', 'publications'),
        'file_sets': ('FileSet', 'publications')
    }

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
            'description': 'The year the publication was published.',
            'notSubmittable': True,
        }
    )
    def publication_year(self, date_published):
        year = datetime.strptime(date_published, '%Y-%m-%d').year
        return year

    @calculated_property(schema={
        'title': 'Samples',
        'type': 'array',
        'description': 'The samples associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Sample',
            'type': ['string', 'object'],
            'linkFrom': 'Sample.publications',
        },
        'notSubmittable': True
    })
    def samples(self, request, samples):
        return paths_filtered_by_status(request, samples)

    @calculated_property(schema={
        'title': 'Donors',
        'type': 'array',
        'description': 'The donors associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Donor',
            'type': ['string', 'object'],
            'linkFrom': 'Donor.publications',
        },
        'notSubmittable': True
    })
    def donors(self, request, donors):
        return paths_filtered_by_status(request, donors)

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'description': 'The file sets associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'FileSet',
            'type': ['string', 'object'],
            'linkFrom': 'FileSet.publications',
        },
        'notSubmittable': True
    })
    def file_sets(self, request, file_sets):
        return paths_filtered_by_status(request, file_sets)
