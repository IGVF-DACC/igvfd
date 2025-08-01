import pytest


def test_types_index_file_inherited_properties(testapp, index_file_bai, alignment_file, reference_file, reference_file_two):
    testapp.patch_json(
        reference_file['@id'],
        {
            'assembly': 'GRCh38',
            'content_type': 'genome reference'
        }
    )
    testapp.patch_json(
        reference_file_two['@id'],
        {
            'transcriptome_annotation': 'GENCODE 43'
        }
    )
    testapp.patch_json(
        alignment_file['@id'],
        {
            'reference_files': [reference_file['@id'], reference_file_two['@id']]
        }
    )
    res = testapp.get(index_file_bai['@id'])
    assert res.json.get('assembly') == 'GRCh38'
    assert res.json.get('transcriptome_annotation') == 'GENCODE 43'
    assert res.json.get('filtered') is False
    assert res.json.get('redacted') is False


def test_types_index_file_summary(testapp, index_file_bai, alignment_file):
    res = testapp.get(index_file_bai['@id'])
    assert res.json.get('summary') == f'index of {alignment_file["accession"]}'
