import pytest


@pytest.fixture
def human_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Homo sapiens',
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
def human_donor_v2(human_donor, document_v1, phenotype_term_alzheimers):
    item = human_donor.copy()
    item.update({
        'schema_version': '2',
        'external_resources': [
            {
                'resource_name': '{control region, restriction length polymorphism RFLP} [human, Senegalese Mandenka West African population sample, Mitochondrial, 89 nt]',
                'resource_identifier': 'GenBank: S77007.2',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S77007.2'
            }
        ],
        'aliases': ['igvf:human_donor_v2'],
        'collections': ['ENCODE'],
        'alternate_accessions': ['IGVFDO111XXX'],
        'documents': [document_v1['@id']],
        'references': ['PMID123'],
        'traits': [phenotype_term_alzheimers['@id']]
    })
    return item
