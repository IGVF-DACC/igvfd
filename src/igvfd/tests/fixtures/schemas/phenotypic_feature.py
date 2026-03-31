import pytest


@pytest.fixture
def phenotypic_feature_basic(
    testapp,
    phenotype_term_ncit_feature,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'feature': phenotype_term_ncit_feature['@id']
    }
    return testapp.post_json('/phenotypic_feature', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotypic_feature_01(
    testapp,
    phenotype_term_alzheimers,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'feature': phenotype_term_alzheimers['@id']
    }
    return testapp.post_json('/phenotypic_feature', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotypic_feature_with_quality(
    testapp,
    phenotype_term_neuritic_plaque_measurement,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'feature': phenotype_term_neuritic_plaque_measurement['@id'],
        'quality': 'frequent'
    }
    return testapp.post_json('/phenotypic_feature', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotypic_feature_with_quantity(
    testapp,
    phenotype_term_mini_mental_status_exam,
    award,
    lab
):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'feature': phenotype_term_mini_mental_status_exam['@id'],
        'quantity': 28,
        'quantity_units': 'MMSE'
    }
    return testapp.post_json('/phenotypic_feature', item, status=201).json['@graph'][0]


@pytest.fixture
def phenotypic_feature_v1(phenotypic_feature_basic):
    item = phenotypic_feature_basic.copy()
    item.update({
        'schema_version': '1',
        'description': ''
    })
    return item


@pytest.fixture
def phenotypic_feature_v3(phenotypic_feature_basic):
    item = phenotypic_feature_basic.copy()
    item.update({
        'schema_version': '3',
        'quality': '2/2'
    })
    return item
