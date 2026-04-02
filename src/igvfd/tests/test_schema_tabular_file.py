import pytest


def test_tabular_file_reference_files_requirement(testapp, reference_file, tabular_file_onlist_1, tabular_file_onlist_2, tabular_file_barcode_replacement, tabular_file):
    # Dependency can be met by specifying submitted_assembly.
    res = testapp.patch_json(
        tabular_file_onlist_1['@id'],
        {'content_type': 'peaks'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tabular_file_onlist_1['@id'],
        {'content_type': 'peaks', 'submitted_assembly': 'unknown'})
    assert res.status_code == 200
    # Dependency can be met by specifying submitted_transcriptome_annotation.
    res = testapp.patch_json(
        tabular_file_onlist_2['@id'],
        {'content_type': 'peaks'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tabular_file_onlist_2['@id'],
        {'content_type': 'peaks', 'submitted_transcriptome_annotation': 'unknown'})
    assert res.status_code == 200
    # Dependency can be met by specifying reference_files.
    res = testapp.patch_json(
        tabular_file_barcode_replacement['@id'],
        {'content_type': 'peaks'}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        tabular_file_barcode_replacement['@id'],
        {'content_type': 'peaks', 'reference_files': [reference_file['@id']]})
    assert res.status_code == 200
    # For excluded content_types, reference_files are not required, but can stil be submitted.
    res = testapp.patch_json(
        tabular_file['@id'],
        {'content_type': 'barcode onlist'})
    assert res.status_code == 200
