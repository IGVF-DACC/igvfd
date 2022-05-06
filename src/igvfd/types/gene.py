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
    name='genes',
    unique_key='gene:geneid',
    properties={
        'title': 'Genes',
        'description': 'Listing of genes',
    })
class Gene(SharedItem):
    item_type = 'gene'
    schema = load_schema('igvfd:schemas/gene.json')
    name_key = 'geneid'

    @calculated_property(schema={
        'title': 'Title',
        'type': 'string',
    })
    def title(self, request, organism, symbol):
        return u'{} ({})'.format(symbol, organism)
