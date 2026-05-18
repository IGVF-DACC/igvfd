import pytest


def test_audit_analysis_step_version_missing_workflows(
    testapp,
    analysis_step_version_3,
    analysis_step_version,
    base_workflow
):
    res = testapp.get(analysis_step_version_3['@id'] + '@@audit')
    assert any(
        error['category'] == 'missing workflows'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
    res = testapp.get(analysis_step_version['@id'] + '@@audit')
    print(res)
    assert all(
        error['category'] != 'missing workflows'
        for error in res.json['audit'].get('NOT_COMPLIANT', [])
    )
