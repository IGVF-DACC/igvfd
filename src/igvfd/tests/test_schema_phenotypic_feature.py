import pytest


def test_phenotypic_feature_quantity_units(
    testapp,
    phenotypic_feature_basic
):
    # Quantity requires Quantity Units
    res = testapp.patch_json(
        phenotypic_feature_basic['@id'],
        {
            'quantity': 70
        },
        expect_errors=True
    )
    assert res.status_code == 422

    # Quantity Units requires Quantity
    res = testapp.patch_json(
        phenotypic_feature_basic['@id'],
        {
            'quantity_units': 'kilogram'
        },
        expect_errors=True
    )
    assert res.status_code == 422

    res = testapp.patch_json(
        phenotypic_feature_basic['@id'],
        {
            'quantity': 70,
            'quantity_units': 'kilogram'
        }
    )
    assert res.status_code == 200
