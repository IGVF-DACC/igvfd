import pytest


def test_treatment_duration_dependency(treatment_2, testapp):
    res = testapp.patch_json(
        treatment_2['@id'],
        {'duration': 15}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        treatment_2['@id'],
        {'duration': 15, 'duration_units': 'minute'})
    assert(res.status_code == 200)


def test_treatment_post_treatment_time_dependency(treatment_2, testapp):
    res = testapp.patch_json(
        treatment_2['@id'],
        {'post_treatment_time': 10}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        treatment_2['@id'],
        {'post_treatment_time': 10, 'post_treatment_time_units': 'hour'})
    assert(res.status_code == 200)


def test_treatment_type_dependency(treatment_1, testapp):
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'chemical', 'treatment_term_id': 'CHEBI:24996'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'protein', 'treatment_term_id': 'UniProtKB:P09919'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'protein', 'treatment_term_id': 'NTR:0001182'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'chemical', 'treatment_term_id': 'NTR:0001181'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'chemical', 'treatment_term_id': 'UniProtKB:P09919'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        treatment_1['@id'],
        {'treatment_type': 'protein', 'treatment_term_id': 'CHEBI:24996'}, expect_errors=True)
    assert(res.status_code == 422)
