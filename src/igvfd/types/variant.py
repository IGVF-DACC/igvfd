from this import d
from snovault import (
    collection,
    load_schema,
    abstract_collection,
    calculated_property
)
from .base import (
    Item
)


@abstract_collection(
    name='variants',
    unique_key='uuid',
    properties={
        'title': 'Variant',
        'description': 'Listing of variants',
    })
class Variant(Item):
    item_type = 'variant'
    base_types = ['Variant'] + Item.base_types
    schema = load_schema('igvfd:schemas/variant.json')

    @calculated_property(
        schema={
            'title': 'Variation Type',
            'type': 'string',
            'enum': [
                'SNV',
                'MNV',
                'insertion',
                'deletion',
                'indel'
            ],
            'notSubmittable': True,
        }
    )
    def variation_type(self, ref, alt):
        if ref == '-':
            return 'insertion'
        elif alt == '-':
            return 'deletion'
        elif len(ref) == len(alt):
            if len(ref) == 1:
                return 'SNV'
            else:
                return 'MNV'
        else:
            return 'indel'


@collection(
    name='human-genomic-variants',
    unique_key='human_genomic_variant:rsid_alt',
    properties={
        'title': 'Human genomic variant',
        'description': 'Listing of human genomic variants',
    })
class HumanGenomicVariant(Variant):
    item_type = 'human_genomic_variant'
    schema = load_schema('igvfd:schemas/human_genomic_variant.json')

    def unique_keys(self, properties):
        keys = super(HumanGenomicVariant, self).unique_keys(properties)
        if 'rsid' in properties:
            value = u'{rsid}/{alt}'.format(**properties)
            keys.setdefault('human_genomic_variant:rsid_alt', []).append(value)
        return keys


@collection(
    name='human-protein-variants',
    unique_key='human_protein_variant:rsid_alt',
    properties={
        'title': 'Human protein variant',
        'description': 'Listing of human protein variants',
    })
class HumanProteinVariant(Variant):
    item_type = 'human_protein_variant'
    schema = load_schema('igvfd:schemas/human_protein_variant.json')

    def unique_keys(self, properties):
        keys = super(HumanProteinVariant, self).unique_keys(properties)
        if 'rsid' in properties:
            value = u'{rsid}/{alt}'.format(**properties)
            keys.setdefault('human_protein_variant:rsid_alt', []).append(value)
        return keys
