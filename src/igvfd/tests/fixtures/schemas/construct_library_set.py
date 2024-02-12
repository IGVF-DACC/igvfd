import pytest


@pytest.fixture
def construct_library_set_genome_wide(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'guide library',
        'scope': 'genome-wide',
        'selection_criteria': [
            'TF binding sites'
        ],
        'product_id': 'addgene:81225',
        'lower_bound_guide_coverage': 15,
        'upper_bound_guide_coverage': 20,
        'guide_type': 'sgRNA'
    }
    return testapp.post_json('/construct_library_set', item).json['@graph'][0]


@pytest.fixture
def base_expression_construct_library_set(testapp, lab, award, gene_myc_hs):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'expression vector library',
        'scope': 'exon',
        'exon': 'E3',
        'small_scale_gene_list': [gene_myc_hs['@id']],
        'selection_criteria': [
            'genes'
        ]
    }
    return testapp.post_json('/construct_library_set', item).json['@graph'][0]


@pytest.fixture
def construct_library_set_reporter(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'reporter library',
        'scope': 'genome-wide',
        'selection_criteria': [
            'accessible genome regions'
        ],
        'average_insert_size': 50
    }
    return testapp.post_json('/construct_library_set', item).json['@graph'][0]


@pytest.fixture
def construct_library_set_y2h(testapp, lab, award, gene_myc_hs, gene_CRLF2_par_y):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'expression vector library',
        'scope': 'genes',
        'small_scale_gene_list': [gene_myc_hs['@id'], gene_CRLF2_par_y['@id']],
        'selection_criteria': [
            'protein interactors'
        ]
    }
    return testapp.post_json('/construct_library_set', item).json['@graph'][0]


@pytest.fixture
def construct_library_set_tile(testapp, lab, award, gene_myc_hs):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'expression vector library',
        'scope': 'tile',
        'tile': {'tile_id': 'tile2', 'tile_start': 91, 'tile_end': 250},
        'small_scale_gene_list': [gene_myc_hs['@id']],
        'selection_criteria': [
            'sequence variants'
        ]
    }
    return testapp.post_json('/construct_library_set', item).json['@graph'][0]


@pytest.fixture
def construct_library_set_v1(testapp, lab, award, gene_myc_hs):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'file_set_type': 'expression vector library',
        'scope': 'exon',
        'exon': '',
        'genes': [gene_myc_hs['@id']],
        'selection_criteria': [
            'genes'
        ]
    }
    return item


@pytest.fixture
def construct_library_set_v2(construct_library_set_v1):
    item = construct_library_set_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def construct_library_set_v3(construct_library_set_v2):
    item = construct_library_set_v2.copy()
    item.update({
        'schema_version': '3'
    })
    return item


@pytest.fixture
def construct_library_set_v4(construct_library_set_genome_wide, gene_myc_hs):
    item = construct_library_set_genome_wide.copy()
    item.update({
        'schema_version': '4',
        'genes': [gene_myc_hs['@id']],
    })
    return item
