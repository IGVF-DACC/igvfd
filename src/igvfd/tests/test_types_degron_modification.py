import pytest


def test_degron_modification_summary(testapp, degron_modification):
    res = testapp.get(degron_modification['@id'])
    assert res.json.get('summary') == 'AID system targeting MYC'
    testapp.patch_json(
        degron_modification['@id'],
        {
            'activated': False,
            'activating_agent_term_id': 'CHEBI:22676',
            'activating_agent_term_name': 'auxin'
        }
    )
    res = testapp.get(degron_modification['@id'])
    assert res.json.get('summary') == 'inactive AID system targeting MYC'
