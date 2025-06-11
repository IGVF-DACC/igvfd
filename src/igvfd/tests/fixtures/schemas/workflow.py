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
def base_workflow_2(testapp, award, lab):
    item = {
        'accession': 'IGVFWF0001WORK',
        'name': 'Base Workflow 2',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/workflow', item).json['@graph'][0]


@pytest.fixture
def base_workflow_3(testapp, award, lab, analysis_step_version_3):
    item = {
        'accession': 'IGVFWF0002WORK',
        'name': 'Base Workflow 3',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step_versions': [analysis_step_version_3['@id']],
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


@pytest.fixture
def workflow_v4(base_workflow):
    item = base_workflow.copy()
    item.update({
        'schema_version': '4',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def workflow_v5(base_workflow):
    item = base_workflow.copy()
    item.update({
        'schema_version': '5',
        'workflow_version': 5
    })
    return item
