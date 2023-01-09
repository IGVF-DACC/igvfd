import pytest


@pytest.fixture
def rodent_donor(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain1',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor_1(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain2',
        'sex': 'female'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor_2(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain3',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def parent_rodent_donor_3(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain4',
        'sex': 'male'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def rodent_donor_orphan(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'taxa': 'Mus musculus',
        'strain': 'strain5',
        'sex': 'female'
    }
    return testapp.post_json('/rodent_donor', item, status=201).json['@graph'][0]


@pytest.fixture
def rodent_donor_v1(rodent_donor):
    item = rodent_donor.copy()
    item.update({
        'schema_version': '1',
        'documents': [],
        'parents': [],
        'external_resources': [],
        'aliases': [],
        'collections': [],
        'alternate_accessions': [],
        'references': []
    })
    return item


@pytest.fixture
def rodent_donor_v2(rodent_donor, document_v1, phenotype_term_alzheimers):
    item = rodent_donor.copy()
    item.update({
        'schema_version': '2',
        'external_resources': [
            {
                'resource_name': '{control region, restriction length polymorphism RFLP} [human, Senegalese Mandenka West African population sample, Mitochondrial, 89 nt]',
                'resource_identifier': 'GenBank: S77007.2',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S77007.2'
            }
        ],
        'aliases': ['igvf:rodent_donor_v2'],
        'collections': ['ENCODE'],
        'alternate_accessions': ['IGVFDO999ZZZ'],
        'documents': [document_v1['@id']],
        'references': ['PMID123'],
        'traits': [phenotype_term_alzheimers['@id']]
    })
    return item
