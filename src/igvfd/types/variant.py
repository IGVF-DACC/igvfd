from snovault import (
    collection,
    load_schema,
    abstract_collection,
    calculated_property
)
from .base import (
    Item
)
from snovault.util import Path


@abstract_collection(
    name='variants',
    unique_key='uuid',
    properties={
        'title': 'Variant',
        'description': 'Listing of variants',
    }
)
class Variant(Item):
    item_type = 'variant'
    base_types = ['Variant'] + Item.base_types
    schema = load_schema('igvfd:schemas/variant.json')
    embedded_with_frame = [
        Path('submitted_by', include=['@id', 'title']),
    ]


@collection(
    name='human-genomic-variants',
    unique_key='human_genomic_variant:sequence_position_ref_alt',
    properties={
        'title': 'Human Genomic Variants',
        'description': 'Listing of human genomic variants',
    }
)
class HumanGenomicVariant(Variant):
    item_type = 'human_genomic_variant'
    schema = load_schema('igvfd:schemas/human_genomic_variant.json')
    embedded_with_frame = Variant.embedded_with_frame

    def unique_keys(self, properties):
        keys = super(HumanGenomicVariant, self).unique_keys(properties)
        if 'refseq_id' in properties:
            value = u'{refseq_id}/{position}/{ref}/{alt}'.format(**properties)
            keys.setdefault('human_genomic_variant:sequence_position_ref_alt', []).append(value)
        elif 'reference_sequence' in properties:
            value = u'{reference_sequence}/{position}/{ref}/{alt}'.format(**properties)
            keys.setdefault('human_genomic_variant:sequence_position_ref_alt', []).append(value)
        return keys
