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
        'file_sets': ('FileSet', 'publications'),
        'workflows': ('Workflow', 'publications'),
        'software': ('Software', 'publications'),
        'software_versions': ('SoftwareVersion', 'publications'),
    }

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super(Publication, self).unique_keys(properties)
        if properties.get('publication_identifiers'):
            keys.setdefault('alias', []).extend(properties['publication_identifiers'])
        return keys

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the publication.',
            'notSubmittable': True,
        }
    )
    def summary(self, title):
        if title:
            return title
        else:
            return self.uuid

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
            'type': 'string',
            'linkFrom': 'Sample.publications',
        },
        'notSubmittable': True
    })
    def samples(self, request, samples):
        return paths_filtered_by_status(request, samples) or None

    @calculated_property(schema={
        'title': 'Donors',
        'type': 'array',
        'description': 'The donors associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Donor',
            'type': 'string',
            'linkFrom': 'Donor.publications',
        },
        'notSubmittable': True
    })
    def donors(self, request, donors):
        return paths_filtered_by_status(request, donors) or None

    @calculated_property(schema={
        'title': 'File Sets',
        'type': 'array',
        'description': 'The file sets associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'File Set',
            'type': 'string',
            'linkFrom': 'FileSet.publications',
        },
        'notSubmittable': True
    })
    def file_sets(self, request, file_sets):
        return paths_filtered_by_status(request, file_sets) or None

    @calculated_property(schema={
        'title': 'Workflows',
        'type': 'array',
        'description': 'The workflows associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Workflow',
            'type': 'string',
            'linkFrom': 'Workflow.publications',
        },
        'notSubmittable': True
    })
    def workflows(self, request, workflows):
        return paths_filtered_by_status(request, workflows) or None

    @calculated_property(schema={
        'title': 'Software',
        'type': 'array',
        'description': 'The software associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Software',
            'type': 'string',
            'linkFrom': 'Software.publications',
        },
        'notSubmittable': True
    })
    def software(self, request, software):
        return paths_filtered_by_status(request, software) or None

    @calculated_property(schema={
        'title': 'Software Versions',
        'type': 'array',
        'description': 'The software versions associated with this publication.',
        'minItems': 1,
        'uniqueItems': True,
        'items': {
            'title': 'Software Version',
            'type': 'string',
            'linkFrom': 'SoftwareVersion.publications',
        },
        'notSubmittable': True
    })
    def software_versions(self, request, software_versions):
        return paths_filtered_by_status(request, software_versions) or None
