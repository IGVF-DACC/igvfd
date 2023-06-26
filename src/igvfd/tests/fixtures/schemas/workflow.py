import pytest


@pytest.fixture
def base_workflow(testapp, award, lab):
    item = {
        'accession': 'IGVFWF0000WRKF',
        'name': 'Base Workflow',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/workflow', item).json['@graph'][0]
