import pytest


@pytest.fixture
def analysis_step_version(testapp, lab, award, analysis_step, software_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step': analysis_step['@id'],
        'software_versions': [software_version['@id']],
        'creation_timestamp': '2023-07-12T16:03:59.940868+00:00'
    }
    return testapp.post_json('/analysis_step_version', item).json['@graph'][0]


@pytest.fixture
def analysis_step_version_2(testapp, lab, award, analysis_step_2, software_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step': analysis_step_2['@id'],
        'software_versions': [software_version['@id']],
        'creation_timestamp': '2023-07-12T16:03:59.940868+00:00'
    }
    return testapp.post_json('/analysis_step_version', item).json['@graph'][0]


@pytest.fixture
def analysis_step_version_3(testapp, lab, award, analysis_step_3, software_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step': analysis_step_3['@id'],
        'software_versions': [software_version['@id']],
        'creation_timestamp': '2024-07-12T16:03:59.940868+00:00'
    }
    return testapp.post_json('/analysis_step_version', item).json['@graph'][0]
