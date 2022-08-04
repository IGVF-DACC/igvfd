from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    SharedItem,
    paths_filtered_by_status,
)


@collection(
    name='variants',
    unique_key='uuid',
    properties={
        'title': 'Genes',
        'description': 'Listing of genes',
    })
class Variant(SharedItem):
    item_type = 'gene'
    schema = load_schema('igvfd:schemas/gene.json')
    name_key = 'geneid'
