import pytest


def test_post_construct_library_set(award, lab, testapp):
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'guide library',
            'scope': 'genome-wide',
            'selection_criteria': ['transcription start sites'],
            'guide_type': 'sgRNA'
        })
    assert res.status_code == 201


def test_dependencies_pseudobulk_set(testapp, pseudobulk_set_base, pseudobulk_set_2):
    res = testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'input_file_sets': [pseudobulk_set_2['@id']]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        pseudobulk_set_base['@id'],
        {'input_file_sets': [pseudobulk_set_2['@id']],
         'merged': True
         })
    assert res.status_code == 200
