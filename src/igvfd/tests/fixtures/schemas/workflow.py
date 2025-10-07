import pytest


@pytest.fixture
def base_workflow_no_asv(testapp, award, lab):
    item = {
        'accession': 'IGVFWF0000WRKF',
        'name': 'Base Workflow',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id']
    }
    return testapp.post_json('/workflow', item).json['@graph'][0]


@pytest.fixture
def base_workflow(testapp, award, lab, analysis_step_version):
    item = {
        'accession': 'IGVFWF0000WRKF',
        'name': 'Base Workflow',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step_versions': [analysis_step_version['@id']],
    }
    return testapp.post_json('/workflow', item).json['@graph'][0]


@pytest.fixture
def base_workflow_2(testapp, award, lab, analysis_step_version_2):
    item = {
        'accession': 'IGVFWF0001WORK',
        'name': 'Base Workflow 2',
        'source_url': 'https://github.com/IGVF-DACC/igvfd',
        'award': award['@id'],
        'lab': lab['@id'],
        'analysis_step_versions': [analysis_step_version_2['@id']],
    }
    return testapp.post_json('/workflow', item).json['@graph'][0]


@pytest.fixture
def workflow_uniform_pipeline(testapp, award, lab, analysis_step_version):
    item = {
        'accession': 'IGVFWF0000MPRA',
        'name': 'MPRAsnakeflow',
        'source_url': 'https://github.com/kircherlab/MPRAsnakeflow/releases/tag/v0.3.0',
        'award': award['@id'],
        'lab': lab['@id'],
        'uniform_pipeline': True,
        'analysis_step_versions': [analysis_step_version['@id']]
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


@pytest.fixture
def workflow_v6(base_workflow):
    item = base_workflow.copy()
    item.update({
        'schema_version': '6',
        'preferred_assay_titles': ['10x Scale pre-indexing']
    })
    return item
