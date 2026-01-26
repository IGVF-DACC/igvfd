from snovault import (
    calculated_property,
    collection,
    load_schema,
)
from .base import (
    SharedItem,
)
from snovault.util import Path


@collection(
    name='genes',
    unique_key='geneid:allele',
    properties={
        'title': 'Genes',
        'description': 'Listing of genes',
    }
)
class Gene(SharedItem):
    item_type = 'gene'
    schema = load_schema('igvfd:schemas/gene.json')
    name_key = 'geneid_with_allele'
    embedded_with_frame = [
        Path('submitted_by', include=['@id', 'title']),
    ]

    set_status_up = []
    set_status_down = []

    def unique_keys(self, properties):
        keys = super().unique_keys(properties)
        geneid = properties.get('geneid')
        allele = properties.get('allele')
        if geneid:
            geneid_with_allele = f'{geneid}-{allele}' if allele else geneid
            keys.setdefault('geneid:allele', []).append(geneid_with_allele)
        return keys

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
        'description': 'The ENSEMBL GeneID concatenated with its version number.',
        'notSubmittable': True,
    })
    def geneid_with_version(self, request, geneid, version_number=None):
        corrected_geneid = None
        if geneid.endswith('_PAR_Y'):
            corrected_geneid = geneid.split('_')[0]

        if version_number is not None:
            if corrected_geneid:
                return u'{}.{}_PAR_Y'.format(corrected_geneid, version_number)
            else:
                return u'{}.{}'.format(geneid, version_number)
        else:
            return geneid

    @calculated_property(
        schema={
            'title': 'Summary',
            'type': 'string',
            'notSubmittable': True,
        }
    )
    def summary(self, symbol, geneid, taxa, allele=None):
        if allele:
            return f'{symbol} {allele} allele - {geneid} ({taxa})'
        else:
            return f'{symbol} - {geneid} ({taxa})'

    @calculated_property(schema={
        'title': 'ENSEMBL GeneID With Allele',
        'type': 'string',
        'description': 'The ENSEMBL GeneID concatenated with its allele info.',
        'notSubmittable': True,
    })
    def geneid_with_allele(self, geneid, allele=None):
        if allele:
            return f'{geneid}-{allele}'
        else:
            return f'{geneid}'
