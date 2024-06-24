import pytest


@pytest.fixture
def analysis_step_version(testapp, lab, award, analysis_step, software_version):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step': analysis_step['@id'],
        'software_versions': [software_version['@id']]
    }
    return testapp.post_json('/analysis_step_version', item).json['@graph'][0]
