import pytest


def test_dependencies_prediction_set(testapp, gene_myc_hs, base_prediction_set, prediction_set_functional_effect, prediction_set_activity_level, tabular_file):
    res = testapp.patch_json(
        base_prediction_set['@id'],
        {'scope': 'loci'
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        base_prediction_set['@id'],
        {'scope': 'genome-wide',
         'small_scale_loci_list': [{'assembly': 'GRCh38',
                                    'chromosome': 'chr9',
                                    'start': 1,
                                    'end': 3500
                                    }]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        base_prediction_set['@id'],
        {'scope': 'loci',
         'small_scale_loci_list': [{'assembly': 'GRCh38',
                                    'chromosome': 'chr9',
                                    'start': 1,
                                    'end': 3500
                                    }]
         })
    assert res.status_code == 200
    res = testapp.patch_json(
        prediction_set_activity_level['@id'],
        {'scope': 'loci',
         'large_scale_loci_list': tabular_file['@id']
         })
    assert res.status_code == 200
    res = testapp.patch_json(
        prediction_set_functional_effect['@id'],
        {'scope': 'loci',
         'small_scale_loci_list': [{'assembly': 'GRCh38',
                                    'chromosome': 'chr9',
                                    'start': 1,
                                    'end': 3500
                                    }]
         })
    assert res.status_code == 200


def test_sample_donor_dependency(testapp, lab, award, tissue, human_donor):
    item = {
        'lab': lab['@id'],
        'award': award['@id'],
        'file_set_type': 'functional effect',
    }
    response = testapp.post_json('/prediction_set', item, expect_errors=True)
    assert response.status_code == 422
    item = {
        'lab': lab['@id'],
        'award': award['@id'],
        'file_set_type': 'functional effect',
        'samples': [tissue['@id']]
    }
    response = testapp.post_json('/prediction_set', item)
    assert response.status_code == 201
    item = {
        'lab': lab['@id'],
        'award': award['@id'],
        'file_set_type': 'functional effect',
        'donors': [human_donor['@id']]
    }
    response = testapp.post_json('/prediction_set', item)
    assert response.status_code == 201
    item = {
        'lab': lab['@id'],
        'award': award['@id'],
        'file_set_type': 'functional effect',
        'samples': [tissue['@id']],
        'donors': [human_donor['@id']]
    }
    response = testapp.post_json('/prediction_set', item, expect_errors=True)
    assert response.status_code == 422
