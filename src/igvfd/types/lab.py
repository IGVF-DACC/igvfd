from snovault import (
    collection,
    load_schema,
    calculated_property
)
from snovault.util import Path
from .base import (
    Item,
    paths_filtered_by_status,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='labs',
    unique_key='lab:name',
    properties={
        'title': 'Labs',
        'description': 'Listing of labs',
    }
)
class Lab(Item):
    item_type = 'lab'
    schema = load_schema('igvfd:schemas/lab.json')
    name_key = 'name'
    embedded_with_frame = [
        Path('awards', include=['@id', 'name', 'component']),
    ]

    @calculated_property(
        schema={
            'title': 'Title',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def title(self, request, pi, institute_label):
        pi_object = request.embed(pi, '@@object')
        pi_name = pi_object.get('title')
        return f'{pi_name}, {institute_label}'
