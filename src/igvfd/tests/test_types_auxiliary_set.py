import pytest


def test_measurement_sets_reverse_link(testapp, measurement_set, measurement_set_mpra, base_auxiliary_set):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    assert set([file_set_id['@id'] for file_set_id in res.json.get('measurement_sets')]
               ) == {measurement_set['@id'], measurement_set_mpra['@id']}


def test_summary(testapp, measurement_set, measurement_set_mpra, measurement_set_multiome, base_auxiliary_set):
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    print(res.json.get('summary'))
    measurement_set_summary = measurement_set.json.get('summary')
    measurement_set_mpra_summary = measurement_set_mpra.json.get('summary')
    assert res.json.get('summary') == f'gRNA sequencing for {measurement_set_summary}, {measurement_set_mpra_summary}'
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    print(res.json.get('summary'))
    assert res.json.get(
        'summary') == f'gRNA sequencing for {measurement_set_summary}, {measurement_set_mpra_summary}, ... and 1 more measurement set'
