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


def test_dependencies_construct_library_set(award, lab, testapp, gene_myc_hs,
                                            construct_library_set_genome_wide,
                                            base_expression_construct_library_set,
                                            construct_library_set_reporter):
    res = testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'scope': 'genes'
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'scope': 'loci',
         'tiling_modality': 'sparse peaks',
         'average_guide_coverage': 10,
         'average_insert_size': 90
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'scope': 'loci',
         'genes': [gene_myc_hs['@id']],
         'average_insert_size': 90
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_set_genome_wide['@id'],
        {'scope': 'genome-wide',
         'loci': [{'assembly': 'GRCh38',
                   'chromosome': 'chr9',
                   'start': 1,
                   'end': 3500
                   }]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_set_reporter['@id'],
        {'scope': 'genes',
         'genes': [gene_myc_hs['@id']]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_set_reporter['@id'],
        {'scope': 'genome-wide',
         'tiling_modality': 'sparse peaks',
         'average_guide_coverage': 10
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_set_reporter['@id'],
        {'scope': 'loci',
         'loci': [{'assembly': 'GRCh38',
                   'chromosome': 'chr9',
                   'start': 1,
                   'end': 3500
                   }]
         })
    assert res.status_code == 200
    res = testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'scope': 'genome-wide'
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        base_expression_construct_library_set['@id'],
        {'scope': 'exon',
         'genes': [gene_myc_hs['@id']]
         }, expect_errors=True)
    assert res.status_code == 200
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'exon',
            'selection_criteria': ['transcription start sites'],
            'genes': [gene_myc_hs['@id']]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'exon',
            'selection_criteria': ['transcription start sites'],
            'genes': [gene_myc_hs['@id']],
            'exon': 'E6'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'tile',
            'selection_criteria': ['transcription start sites'],
            'genes': [gene_myc_hs['@id']]
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'tile',
            'selection_criteria': ['transcription start sites'],
            'genes': [gene_myc_hs['@id']],
            'tile': {'tile_id': 'tile1', 'tile_start': 1, 'tile_end': 56}
        })
    assert res.status_code == 201
