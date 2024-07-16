import pytest


def test_degron_modification_summary(testapp, degron_modification, gene_myc_hs):
    res = testapp.get(degron_modification['@id'])
    assert res.json.get('summary') == 'AID system targeting MYC'
