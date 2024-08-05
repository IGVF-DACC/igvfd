from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status
)


@collection(
    name='software',
    unique_key='software:name',
    properties={
        'title': 'Software',
        'description': 'Software pages',
    }
)
class Software(Item):
    item_type = 'software'
    schema = load_schema('igvfd:schemas/software.json')
    name_key = 'name'
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('publications', include=['@id', 'publication_identifiers']),
    ]
    rev = {
        'versions': ('SoftwareVersion', 'software')
    }

    set_status_up = []
    set_status_down = []

    @calculated_property(schema={
        'title': 'Versions',
        'type': 'array',
        'description': 'A list of versions that have been released for this software.',
        'minItems': 1,
        'uniqueItems': True,
        'notSubmittable': True,
        'items': {
            'title': 'Version',
            'type': 'string',
            'linkTo': 'SoftwareVersion'
        }
    })
    def versions(self, request, versions):
        return paths_filtered_by_status(request, versions)

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, title):
        return title
