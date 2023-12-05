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
def phenotypic_feature_v1(phenotypic_feature_basic):
    item = phenotypic_feature_basic.copy()
    item.update({
        'schema_version': '1',
        'description': ''
    })
    return item
