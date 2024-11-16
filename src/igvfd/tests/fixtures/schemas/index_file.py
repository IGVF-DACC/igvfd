import pytest


@pytest.fixture
def index_file_tbi(testapp, lab, award, principal_analysis_set, tabular_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '5ac7f55b8735dd430df19a01b08bb548',
        'file_format': 'tsv',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'index',
        'assembly': 'GRCh38',
        'controlled_access': False,
        'derived_from': [tabular_file['@id']]
    }
    return testapp.post_json('/index_file', item, status=201).json['@graph'][0]


@pytest.fixture
def index_file_bai(testapp, lab, award, principal_analysis_set, alignment_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '07f195481361a5c3a5ac0cf5501b09c',
        'file_format': 'tsv',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'index',
        'assembly': 'GRCh38',
        'controlled_access': False,
        'derived_from': [alignment_file['@id']]
    }
    return testapp.post_json('/index_file', item, status=201).json['@graph'][0]
