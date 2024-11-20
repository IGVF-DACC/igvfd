import pytest


def test_types_index_file_inherited_properties(testapp, index_file_bai, alignment_file):
    testapp.patch_json(
        alignment_file['@id'],
        {
            'transcriptome_annotation': 'GENCODE 43'
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
