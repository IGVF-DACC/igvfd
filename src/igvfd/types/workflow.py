from snovault import (
    collection,
    load_schema
)
from .base import (
    Item
)


@collection(
    name='workflows',
    unique_key='workflow:name',
    properties={
        'title': 'Workflow',
        'description': 'Listing of workflows',
    }
)
class Workflow(Item):
    item_type = 'workflow'
    schema = load_schema('igvfd:schemas/workflow.json')
    name_key = 'name'
