import pytest


def test_patch_cas_species(modification, testapp):
    res = testapp.patch_json(modification['@id'],
                             {'cas_species': 'Streptococcus pyogenes (Sp)'})
    assert res.status_code == 200
    res = testapp.patch_json(modification['@id'],
                             {'cas_species': ''}, expect_errors=True)
    assert res.status_code == 422


def test_read_cas_species(modification, testapp):
    res = testapp.get(modification['@id'])
    assert res.json['cas_species'] == 'Streptococcus pyogenes (Sp)'


def test_cas_species_requirement(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'cas_species': 'Streptococcus pyogenes (Sp)',
        'modality': 'interference'
    }
    res = testapp.post_json('/modification', item)
    assert res.status_code == 201

    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'cas': 'dCas9',
        'modality': 'interference'
    }
    res = testapp.post_json('/modification', item, expect_errors=True)
    assert res.status_code == 422
