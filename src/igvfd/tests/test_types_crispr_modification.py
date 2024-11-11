import pytest


def test_modification_summary(testapp, crispr_modification, gene_myc_hs):
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPRi Sp-dCas9'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'modality': 'activation',
            'fused_domain': 'VP64'
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPRa Sp-dCas9-VP64'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'cas': 'Cas13',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_proteins': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing Sp-Cas13-ANTI-FLAG fused to MYC'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'cas': 'SpG',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_proteins': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpG-ANTI-FLAG fused to MYC'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'cas': 'SpRY',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_proteins': [gene_myc_hs['@id']]
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpRY-ANTI-FLAG fused to MYC'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'activated': False,
            'activating_agent_term_id': 'CHEBI:22676',
            'activating_agent_term_name': 'auxin'
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'inactive CRISPR localizing SpRY-ANTI-FLAG fused to MYC'
