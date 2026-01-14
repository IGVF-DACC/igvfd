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
                                            construct_library_set_reporter, tabular_file, orf_foxp):
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
         'small_scale_gene_list': [gene_myc_hs['@id']],
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
         'small_scale_gene_list': [gene_myc_hs['@id']]
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
         'small_scale_loci_list': [{'assembly': 'GRCh38',
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
         'small_scale_gene_list': [gene_myc_hs['@id']]
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
            'small_scale_gene_list': [gene_myc_hs['@id']]
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
            'small_scale_gene_list': [gene_myc_hs['@id']],
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
            'large_scale_gene_list': tabular_file['@id']
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'genes',
            'selection_criteria': ['transcription start sites'],
            'large_scale_gene_list': tabular_file['@id']
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'control',
            'control_types': ['reference transduction'],
            'selection_criteria': ['TF binding sites'],
            'control_file_sets': [base_expression_construct_library_set['@id']]
        })
    assert res.status_code == 201
    # either small_scale_gene_list or large_scale_gene_list is accepted when scope = 'interactors'
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'interactors',
            'selection_criteria': ['protein interactors'],
            'orf_list': [orf_foxp['@id']],
            'large_scale_gene_list': tabular_file['@id']
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/construct_library_set',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'file_set_type': 'expression vector library',
            'scope': 'interactors',
            'selection_criteria': ['protein interactors'],
            'orf_list': [orf_foxp['@id']],
            'small_scale_gene_list': [gene_myc_hs['@id']]
        })
    assert res.status_code == 201
