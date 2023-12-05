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


@pytest.fixture
def workflow_v1(base_workflow):
    item = base_workflow.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def workflow_v2(workflow_v1):
    item = workflow_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
