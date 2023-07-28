import pytest


@pytest.fixture
def construct_library_genome_wide(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'scope': 'genome-wide',
        'selection_criteria': [
            'TF binding sites'
        ],
        'product_id': 'addgene:81225',
        'guide_library_details': {'lower_bound_guide_coverage': 15,
                                  'upper_bound_guide_coverage': 20,
                                  'guide_type': 'sgRNA'
                                  }
    }
    return testapp.post_json('/construct_library', item).json['@graph'][0]


@pytest.fixture
def base_construct_library(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'scope': 'genome-wide',
        'selection_criteria': [
            'transcription start sites'
        ],
        'guide_library_details': {
            'guide_type': 'sgRNA'
        }
    }
    return testapp.post_json('/construct_library', item).json['@graph'][0]


@pytest.fixture
def construct_library_v1(
        testapp, lab, award, plasmid_map_document, document_v1):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'scope': 'genome-wide',
        'origins': [
            'transcription start sites'
        ],
        'plasmid_map': plasmid_map_document['@id'],
        'documents': [document_v1['@id']]
    }
    return item


@pytest.fixture
def construct_library_v2(
        testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'scope': 'genome-wide'
    }
    return item


@pytest.fixture
def construct_library_v3(
        testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'scope': 'genome-wide',
        'schema_version': '3',
        'origins': ['accessible genome regions']
    }
    return item


@pytest.fixture
def construct_library_v4(testapp, construct_library_genome_wide):
    item = construct_library_genome_wide.copy()
    item.update({
        'schema_version': '4',
        'references': ['10.1101/2023.08.02']
    })
    return item
