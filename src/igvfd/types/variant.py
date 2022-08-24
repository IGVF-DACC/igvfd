from snovault import (
    collection,
    load_schema,
    abstract_collection
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


@collection(
    name='human-variants',
    unique_key='human_variant:rsid_alt',
    properties={
        'title': 'Human variant',
        'description': 'Listing of human variants',
    })
class HumanVariant(Variant):
    item_type = 'human_variant'
    schema = load_schema('igvfd:schemas/human_variant.json')

    def unique_keys(self, properties):
        keys = super(HumanVariant, self).unique_keys(properties)
        value = u'{rsid}/{alt}'.format(**properties)
        keys.setdefault('human_variant:rsid_alt', []).append(value)
        return keys
