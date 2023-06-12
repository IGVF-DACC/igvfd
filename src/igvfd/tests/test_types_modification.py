import pytest


def test_modification_summary(testapp, modification, gene_myc_hs):
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPRi dCas9'

    testapp.patch_json(
        modification['@id'],
        {
            'modality': 'activation',
            'fused_domain': 'VP64'
        }
    )
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPRa dCas9-VP64'

    testapp.patch_json(
        modification['@id'],
        {
            'cas': 'Cas13',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_protein': gene_myc_hs['@id']
        }
    )
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpCas13-ANTI-FLAG fused to MYC'
