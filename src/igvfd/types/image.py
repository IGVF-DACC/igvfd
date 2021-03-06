from snovault import (
    collection,
    calculated_property,
    load_schema,
)
from .base import (
    Item,
)
from snovault.attachment import ItemWithAttachment


@collection(
    name='images',
    unique_key='image:filename',
    properties={
        'title': 'Image',
        'description': 'Listing of portal images',
    })
class Image(ItemWithAttachment, Item):
    item_type = 'image'
    schema = load_schema('igvfd:schemas/image.json')
    schema['properties']['attachment']['properties']['type']['enum'] = [
        'image/png',
        'image/jpeg',
        'image/gif',
    ]

    def unique_keys(self, properties):
        keys = super(Image, self).unique_keys(properties)
        value = properties['attachment']['download']
        keys.setdefault('image:filename', []).append(value)
        return keys

    @calculated_property(schema={
        'title': 'Thumb Nail',
        'description': 'Image url',
        'type': 'string',
    })
    def thumb_nail(self, request, attachment):
        return self.jsonld_id(request) + attachment['href']

    @calculated_property(schema={
        'title': 'Download Url',
        'description': 'Download Url',
        'type': 'string',
    })
    def download_url(self, request, attachment):
        return self.jsonld_id(request) + attachment['href']
