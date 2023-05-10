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
    }
)
class Gene(SharedItem):
    item_type = 'gene'
    schema = load_schema('igvfd:schemas/gene.json')
    name_key = 'geneid'

    @calculated_property(schema={
        'title': 'Title',
        'type': 'string',
        'notSubmittable': True,
    })
    def title(self, request, taxa, symbol):
        return u'{} ({})'.format(symbol, taxa)

    @calculated_property(schema={
        'title': 'ENSEMBL GeneID With Version',
        'type': 'string',
        'notSubmittable': True,
    })
    def geneid_with_version(self, request, geneid, version_number=None):
        if geneid.endswith('_PAR_Y'):
            (corrected_geneid, par_y) = geneid.split('_')

        if version_number is not None:
            if par_y:
                return u'{}.{}_{}'.format(corrected_geneid, version_number, par_y)
            else:
                return u'{}.{}'.format(geneid, version_number)
        else:
            return geneid
