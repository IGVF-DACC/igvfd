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
        error['category'] == 'missing measurement set'
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
        error['category'] != 'missing measurement set'
        for error in res.json['audit'].get('WARNING', [])
    )


def test_audit_missing_input_file_set(
    testapp,
    analysis_set_base,
    measurement_set,
    matrix_file,
    signal_file
):
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': measurement_set['@id']
        }
    )
    testapp.patch_json(
        matrix_file['@id'],
        {
            'file_set': analysis_set_base['@id'],
            'derived_from': [signal_file['@id']]
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        signal_file['@id'],
        {
            'file_set': analysis_set_base['@id']
        }
    )
    res = testapp.get(analysis_set_base['@id'] + '@@audit')
    assert all(
        error['category'] != 'missing input file set'
        for error in res.json['audit'].get('ERROR', [])
    )
