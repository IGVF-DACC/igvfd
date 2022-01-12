from snovault.attachment import ItemWithAttachment
from snovault import (
    collection,
    load_schema,
)
from .base import (
    Item,
    paths_filtered_by_status,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='documents',
    properties={
        'title': 'Documents',
        'description': 'Listing of Biosample Documents',
    })
class Document(ItemWithAttachment, Item):
    item_type = 'document'
    schema = load_schema('igvfd:schemas/document.json')
    embedded = ['lab', 'award', 'submitted_by']
