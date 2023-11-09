import pytest


def test_audit_inconsistent_input_file_sets(
    testapp,
    analysis_set_base,
    curated_set_transcriptome,
    measurement_set
):
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'file_set_type': 'primary analysis',
            'input_file_sets': [curated_set_transcriptome['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent input file sets'
        for error in res.json['audit'].get('WARNING', [])
    )
    testapp.patch_json(
        analysis_set_base['@id'],
        {
            'input_file_sets': [curated_set_transcriptome['@id'], measurement_set['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent input file sets'
        for error in res.json['audit'].get('WARNING', [])
    )
