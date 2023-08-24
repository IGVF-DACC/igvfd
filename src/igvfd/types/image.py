from snovault import (
    collection,
    calculated_property,
    load_schema,
)
from .base import (
    Item,
)
from snovault.attachment import ItemWithAttachment
from snovault.util import Path


@collection(
    name='images',
    unique_key='image:filename',
    properties={
        'title': 'Images',
        'description': 'Listing of portal images',
    }
)
class Image(ItemWithAttachment, Item):
    item_type = 'image'
    schema = load_schema('igvfd:schemas/image.json')
    schema['properties']['attachment']['properties']['type']['enum'] = [
        'image/png',
        'image/jpeg',
        'image/gif',
    ]
    embedded_with_frame = [
        Path('submitted_by', include=['@id', 'title']),
    ]

    def unique_keys(self, properties):
        keys = super(Image, self).unique_keys(properties)
        value = properties['attachment']['download']
        keys.setdefault('image:filename', []).append(value)
        return keys

    @calculated_property(
        schema={
            'title': 'Thumb Nail',
            'description': 'Image url',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def thumb_nail(self, request, attachment):
        return self.jsonld_id(request) + attachment['href']

    @calculated_property(
        schema={
            'title': 'Download Url',
            'description': 'Download Url',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def download_url(self, request, attachment):
        return self.jsonld_id(request) + attachment['href']
