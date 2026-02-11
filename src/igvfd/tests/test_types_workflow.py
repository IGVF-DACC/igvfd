import pytest


def test_summary_workflow(testapp, base_workflow):
    # Workflow without version
    res = testapp.get(base_workflow['@id'])
    assert res.json.get('summary') == 'Base Workflow'
    # Workflow with version
    testapp.patch_json(
        base_workflow['@id'],
        {'workflow_version': 'v1.2.3'}
    )
    res = testapp.get(base_workflow['@id'])
    assert res.json.get('summary') == 'Base Workflow v1.2.3'
