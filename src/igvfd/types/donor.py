from snovault import (
    abstract_collection,
    collection,
    load_schema,
)
from snovault.util import Path
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
    embedded_with_frame = [
        Path('award', include=['@id', 'component']),
        Path('lab', include=['@id', 'title']),
        Path('submitted_by', include=['@id', 'title']),
        Path('phenotypic_features.feature', include=['@id', 'feature', 'term_id',
             'term_name', 'quantity', 'quantity_units', 'observation_date'])
    ]

    set_status_up = []
    set_status_down = []


@collection(
    name='human-donors',
    unique_key='accession',
    properties={
        'title': 'Human Donors',
        'description': 'Listing of human donors',
    }
)
class HumanDonor(Donor):
    item_type = 'human_donor'
    schema = load_schema('igvfd:schemas/human_donor.json')
    embedded_with_frame = Donor.embedded_with_frame + [
        Path('related_donors.donor', include=['@id', 'accession']),
    ]
    audit_inherit = [
        'related_donors.donor'
    ]


@collection(
    name='rodent-donors',
    unique_key='accession',
    properties={
        'title': 'Rodent Donors',
        'description': 'Listing of rodent donors',
    }
)
class RodentDonor(Donor):
    item_type = 'rodent_donor'
    schema = load_schema('igvfd:schemas/rodent_donor.json')
    embedded_with_frame = Donor.embedded_with_frame + [
        Path('sources', include=['@id', 'title']),
    ]

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
