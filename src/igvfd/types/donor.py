from snovault import (
    abstract_collection,
    collection,
    load_schema,
)

from .base import (
    Item,
)


@abstract_collection(
    name='donors',
    unique_key='accession',
    properties={
        'title': 'Donor',
        'description': 'Listing of donors',
    }
)
class Donor(Item):
    item_type = 'donor'
    base_types = ['Donor'] + Item.base_types
    name_key = 'accession'
    schema = load_schema('igvfd:schemas/donor.json')


@collection(
    name='human-donors',
    unique_key='accession',
    properties={
        'title': 'Human donors',
        'description': 'Listing of human donors',
    }
)
class HumanDonor(Donor):
    item_type = 'human_donor'
    schema = load_schema('igvfd:schemas/human_donor.json')


@collection(
    name='rodent-donors',
    unique_key='accession',
    properties={
        'title': 'Rodent donors',
        'description': 'Listing of rodent donors',
    }
)
class RodentDonor(Donor):
    item_type = 'rodent_donor'
    schema = load_schema('igvfd:schemas/rodent_donor.json')

    def unique_keys(self, properties):
        keys = super(RodentDonor, self).unique_keys(properties)
        if properties.get('rodent_identifier'):
            lab = properties.get('lab').split('/')[-1]
            value = f'{lab}:{properties.get("rodent_identifier")}'
            keys.setdefault('rodentdonor:lab_rodentid', []).append(value)
        else:
            value = u'{strain}/{sex}'.format(**properties)
            keys.setdefault('rodentdonor:strain_sex', []).append(value)
        return keys
