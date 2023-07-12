import pytest


def test_post_construct_library(award, lab, testapp):
    res = testapp.post_json(
        '/construct_library',
        {
            'lab': lab['@id'],
            'award': award['@id'],
            'scope': 'genome-wide',
            'origins': ['transcription start sites'],
            'guide_library_details': {
                'guide_type': 'sgRNA'
            }
        })
    assert res.status_code == 201


def test_dependencies_construct_library(award, lab, testapp, gene_myc_hs,
                                        construct_library_genome_wide,
                                        base_construct_library):
    res = testapp.patch_json(
        construct_library_genome_wide['@id'],
        {'scope': 'loci'
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_genome_wide['@id'],
        {'scope': 'loci',
         'guide_library_details': {'tiling_modality': 'sparse peaks',
                                   'average_guide_coverage': 10
                                   },
         'reporter_library_details': {'average_insert_size': 90
                                      }
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        base_construct_library['@id'],
        {'scope': 'loci',
         'expression_vector_library_details': {'cloned_genes': [gene_myc_hs['@id']]
                                               },
         'reporter_library_details': {'average_insert_size': 90
                                      }
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_genome_wide['@id'],
        {'scope': 'genome-wide',
         'targeted_loci': [{'assembly': 'GRCh38',
                            'chromosome': 'chr9',
                            'start': 1,
                            'end': 3500
                            }]
         }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        construct_library_genome_wide['@id'],
        {'scope': 'loci',
         'targeted_loci': [{'assembly': 'GRCh38',
                            'chromosome': 'chr9',
                            'start': 1,
                            'end': 3500
                            }],
         'guide_library_details': {'guide_type': 'pgRNA',
                                   'tiling_modality': 'sparse peaks',
                                   'average_guide_coverage': 10
                                   }
         })
    assert res.status_code == 200
