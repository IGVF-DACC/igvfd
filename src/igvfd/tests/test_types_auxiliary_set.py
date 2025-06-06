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
    res = testapp.get(base_auxiliary_set['@id'])
    assert res.json.get('summary') == 'gRNA sequencing'
    testapp.patch_json(
        measurement_set['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    measurement_set_summary = measurement_set['summary']
    assert res.json.get('summary') == f'gRNA sequencing for {measurement_set_summary}'
    testapp.patch_json(
        measurement_set_mpra['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    measurement_set_mpra_summary = measurement_set_mpra['summary']
    assert measurement_set_summary in res.json.get(
        'summary') and measurement_set_mpra_summary in res.json.get('summary')
    testapp.patch_json(
        measurement_set_multiome['@id'],
        {
            'auxiliary_sets': [base_auxiliary_set['@id']]
        }
    )
    measurement_set_multiome_summary = measurement_set_multiome['summary']
    res = testapp.get(base_auxiliary_set['@id'])
    auxiliary_summary = res.json.get('summary')
    assert auxiliary_summary == 'gRNA sequencing for ATAC-seq (10x multiome), MPRA, STARR-seq'


def test_calculated_donors(testapp, base_auxiliary_set, primary_cell, human_donor, in_vitro_cell_line, rodent_donor):
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'samples': [primary_cell['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {human_donor['@id']}
    testapp.patch_json(
        base_auxiliary_set['@id'],
        {
            'samples': [in_vitro_cell_line['@id']]
        }
    )
    res = testapp.get(base_auxiliary_set['@id'])
    assert set([donor['@id'] for donor in res.json.get('donors')]) == {rodent_donor['@id']}
