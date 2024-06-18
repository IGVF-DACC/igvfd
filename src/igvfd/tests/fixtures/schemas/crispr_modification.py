import pytest


@pytest.fixture
def crispr_modification(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'modality': 'interference',
        'cas_species': 'Streptococcus pyogenes (Sp)'
    }
    return testapp.post_json('/crispr_modification', item, status=201).json['@graph'][0]


@pytest.fixture
def crispr_modification_missing_cas_sp(crispr_modification):
    item = modification.copy()
    item.pop('cas_species', None)
    item.update({
        'schema_version': '1',
        'notes': 'Test.'
    })
    return item


@pytest.fixture
def crispr_modification_v2(crispr_modification, source):
    item = modification.copy()
    item.update({
        'schema_version': '2',
        'source': source['@id']
    })
    return item


@pytest.fixture
def crispr_modification_activation(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'modality': 'activation',
        'cas_species': 'Streptococcus pyogenes (Sp)'
    }
    return testapp.post_json('/crispr_modification', item, status=201).json['@graph'][0]


@pytest.fixture
def crispr_modification_v3(crispr_modification_activation):
    item = modification_activation.copy()
    item.update({
        'schema_version': '3',
        'description': ''
    })
    return item


@pytest.fixture
def crispr_modification_prime_editing(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'nCas9',
        'modality': 'prime editing',
        'fused_domain': 'M-MLV RT (PE2)',
        'cas_species': 'Streptococcus pyogenes (Sp)'
    }
    return testapp.post_json('/crispr_modification', item, status=201).json['@graph'][0]


@pytest.fixture
def crispr_modification_v1_zim3(crispr_modification):
    item = crispr_modification.copy()
    item.update({
        'schema_version': '1',
        'fused_domain': 'ZIM3',
    })
    return item


@pytest.fixture
def crispr_modification_v1_krab(crispr_modification):
    item = crispr_modification.copy()
    item.update({
        'schema_version': '1',
        'fused_domain': 'KRAB',
    })
    return item
