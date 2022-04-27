import pytest


def test_treatment_amount_dependency(testapp):
    item = {
        'treatment_term_name': 'lactate',
        'treatment_term_id': 'CHEBI:24996',
        'treatment_type': 'chemical',
        'amount': '10'
    }
    return testapp.post_json('/treatment', item, expect_errors=True)
    assert res.json['status'] == 422
    item.update(
        {
            'amount_units': 'ng/mL'
        }
    )
    return testapp.post_json('/treatment', item)
    assert res.json['status'] == 200


def test_treatment_duration_dependency(testapp):
    item = {
        'treatment_term_name': 'lactate',
        'treatment_term_id': 'CHEBI:24996',
        'treatment_type': 'chemical',
        'amount': '10',
        'amount_units': 'ng/mL',
        'duration_units': 'hour'
    }
    return testapp.post_json('/treatment', item, expect_errors=True)
    assert res.json['status'] == 422
    item.update(
        {
            'duration': '1'
        }
    )
    return testapp.post_json('/treatment', item)
    assert res.json['status'] == 200


def test_treatment_post_treatment_time_dependency(testapp):
    item = {
        'treatment_term_name': 'lactate',
        'treatment_term_id': 'CHEBI:24996',
        'treatment_type': 'chemical',
        'amount': '10',
        'amount_units': 'ng/mL',
        'post_treatment_time': '10'
    }
    return testapp.post_json('/treatment', item, expect_errors=True)
    assert res.json['status'] == 422
    item.update(
        {
            'post_treatment_time_units': 'minute'
        }
    )
    return testapp.post_json('/treatment', item)
    assert res.json['status'] == 200


def test_treatment_calculated(treatment_1, testapp):
    res = testapp.get(treatment_1['@id'])
    assert(res.json['title'] == 'Treated with 10 mM lactate for 1 hour.')


def test_treatment_no_duration_calculated(treatment_2, testapp):
    res = testapp.get(treatment_2['@id'])
    assert(res.json['title'] == 'Treated with 10 ng/mL G-CSF for non-specified duration.')


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
