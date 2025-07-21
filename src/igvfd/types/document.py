from snovault.attachment import ItemWithAttachment
from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from snovault.util import Path
from .base import (
    Item,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='documents',
    properties={
        'title': 'Documents',
        'description': 'Listing of Biosample Documents',
    }
)
class Document(ItemWithAttachment, Item):
    item_type = 'document'
    schema = load_schema('igvfd:schemas/document.json')
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = []
    set_status_down = []

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'description': 'A summary of the document.',
            'notSubmittable': True,
        }
    )
    def summary(self, description):
        if description:
            return description
        else:
            return self.uuid
