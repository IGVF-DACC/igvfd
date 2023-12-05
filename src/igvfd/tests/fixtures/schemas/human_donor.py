import pytest


@pytest.fixture
def human_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens'
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_1(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_2(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_human_donor_3(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def human_donor_orphan(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def human_male_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
        'sex': 'male'
    }
    return testapp.post_json('/human_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def human_donor_v1(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '1',
        'parents': [],
        'external_resources': [],
        'aliases': [],
        'collections': [],
        'alternate_accessions': [],
        'documents': [],
        'references': []
    })
    return item


@pytest.fixture
def human_donor_v2(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '2',
        'health_status_history': [
            {
                'health_description': 'Running fever 103F, feeling tired',
                'date_start': '2022-01-04',
                'date_end': '2022-01-10'
            },
            {
                'health_description': 'Running fever 103F, feeling tired',
                'date_start': '2021-12-03',
                'date_end': '2022-01-10'
            }
        ]
    })
    return item


@pytest.fixture
def human_donor_v3(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '3',
        'ethnicity': ['Hispanic', 'Han Chinese']
    })
    return item


@pytest.fixture
def human_donor_v4(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '4',
        'accession': 'IGVFDO999HHS'
    })
    return item


@pytest.fixture
def human_donor_v5(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '5',
        'external_resources': [
            {
                'resource_name': '{control region, restriction length polymorphism RFLP} [human, Senegalese Mandenka West African population sample, Mitochondrial, 89 nt]',
                'resource_identifier': 'GenBank: S77007.1',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S77007.1'
            }
        ]
    })
    return item


@pytest.fixture
def human_donor_v6_single_trait_no_notes(human_donor, phenotype_term_alzheimers):
    item = human_donor.copy()
    item.update({
        'schema_version': '6',
        'traits': [
            phenotype_term_alzheimers['@id']
        ]
    })
    return item


@pytest.fixture
def human_donor_v6_multiple_traits_no_notes(human_donor, phenotype_term_alzheimers, phenotype_term_myocardial_infarction):
    item = human_donor.copy()
    item.update({
        'schema_version': '6',
        'traits': [
            phenotype_term_alzheimers['@id'],
            phenotype_term_myocardial_infarction['@id']
        ]
    })
    return item


@pytest.fixture
def human_donor_v6_single_trait_with_notes(human_donor, phenotype_term_alzheimers):
    item = human_donor.copy()
    item.update({
        'schema_version': '6',
        'traits': [
            phenotype_term_alzheimers['@id']
        ],
        'notes': 'This is a note.'
    })
    return item


@pytest.fixture
def human_donor_v7_with_parents(human_donor, parent_human_donor_1, parent_human_donor_2):
    item = human_donor.copy()
    item.update({
        'schema_version': '7',
        'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id']
        ],
    })
    return item


@pytest.fixture
def human_donor_v8(human_donor, parent_human_donor_1, parent_human_donor_2):
    item = human_donor.copy()
    item.update({
        'schema_version': '8',
        'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id']
        ],
    })
    return item


@pytest.fixture
def human_donor_v9(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '9',
        'human_donor_identifier': ['X cell line donor', 'elvis-1']
    })
    return item


@pytest.fixture
def item_donor(human_donor):
    return human_donor


@pytest.fixture
def human_donor_v10(human_donor):
    item = human_donor.copy()
    item.update({
        'schema_version': '10',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def human_donor_v11(human_donor_v10):
    item = human_donor_v10.copy()
    item.update({
        'schema_version': '11',
        'description': ''
    })
    return item
