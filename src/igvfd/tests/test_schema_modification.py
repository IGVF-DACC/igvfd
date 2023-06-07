import pytest


def test_patch_cas_species(modification, testapp):
    res = testapp.patch_json(modification['@id'],
                             {'cas_species': 'Streptococcus pyogenes (Sp)'})
    assert res.status_code == 200
    res = testapp.patch_json(modification['@id'],
                             {'cas_species': ''}, expect_errors=True)
    assert res.status_code == 422


def test_read_cas_species(modification_v2, testapp):
    res = testapp.get(modification_v2['@id'])
    assert res.json['cas_species'] == 'Streptococcus pyogenes (Sp)'
