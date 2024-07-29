import pytest


def test_phenotypic_feature_summary(testapp, phenotypic_feature_basic):
    testapp.patch_json(
        phenotypic_feature_basic['@id'],
        {
            'quantity': 60,
            'quantity_units': 'kilogram',
            'observation_date': '2020-11-03'
        }
    )
    res = testapp.get(phenotypic_feature_basic['@id'])
    assert res.json.get('summary', '') == '60 kilogram Body Weight Measurement observed on 2020-11-03'
