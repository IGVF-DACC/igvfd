from snovault import (
    calculated_property,
    collection,
    load_schema,
)

from .base import (
    Item,
    ALLOW_CURRENT,
    DELETED,
)


@collection(
    name='awards',
    unique_key='award:name',
    properties={
        'title': 'Awards (Grants)',
        'description': 'Listing of awards (aka grants)',
    }
)
class Award(Item):
    item_type = 'award'
    schema = load_schema('igvfd:schemas/award.json')
    name_key = 'name'
    STATUS_ACL = {
        'current': ALLOW_CURRENT,
        'deleted': DELETED,
        'replaced': DELETED,
        'disabled': ALLOW_CURRENT
    }
