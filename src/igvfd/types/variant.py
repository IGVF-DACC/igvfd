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
    name='genomic-human-variants',
    unique_key='genomic_human_variant:rsid_alt',
    properties={
        'title': 'Genomic human variant',
        'description': 'Listing of genomic human variants',
    })
class GenomicHumanVariant(Variant):
    item_type = 'genomic_human_variant'
    schema = load_schema('igvfd:schemas/genomic_human_variant.json')

    def unique_keys(self, properties):
        keys = super(GenomicHumanVariant, self).unique_keys(properties)
        value = u'{rsid}/{alt}'.format(**properties)
        keys.setdefault('genomic_human_variant:rsid_alt', []).append(value)
        return keys
