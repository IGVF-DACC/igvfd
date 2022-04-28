from .base import (
    Item,
)
rom snovault import (
    abstract_collection,
    collection,
    load_schema,
)


@abstract_collection(
    name='donors',
    unique_key='accession',
    properties={
        'title': 'Donor',
        'description': 'Listing of donors',
    })
class Donor(Item):
    item_type = 'donor'
    base_types = ['Donor'] + Item.base_types
    schema = load_schema('igvfd:schemas/donor.json')


@collection(
    name='human-donors',
    unique_key='accession',
    properties={
        'title': 'Human donors',
        'description': 'Listing of human donors',
    })
class HumanDonor(Donor):
    item_type = 'human_donor'
    schema = load_schema('igvfd:schemas/human_donor.json')


@collection(
    name='rodent-donors',
    unique_key='accession',
    properties={
        'title': 'Rodent donors',
        'description': 'Listing of rodent donors',
    })
class RodentDonor(Donor):
    item_type = 'rodent_donor'
    schema = load_schema('igvfd:schemas/rodent_donor.json')
