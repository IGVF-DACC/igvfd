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
    ]
    rev = {
        'versions': ('SoftwareVersion', 'software')
    }

    @calculated_property(schema={
        'title': 'Versions',
        'type': 'array',
        'notSubmittable': True,
        'items': {
            'type': 'string',
            'linkTo': 'SoftwareVersion'
        }
    })
    def versions(self, request, versions):
        return paths_filtered_by_status(request, versions)
