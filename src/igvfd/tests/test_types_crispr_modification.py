import pytest


def test_modification_summary(testapp, crispr_modification, gene_myc_hs):
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPRi SpdCas9'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'modality': 'activation',
            'fused_domain': 'VP64'
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPRa SpdCas9-VP64'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'cas': 'Cas13',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_protein': gene_myc_hs['@id']
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpCas13-ANTI-FLAG fused to MYC'

    testapp.patch_json(
        crispr_modification['@id'],
        {
            'cas': 'SpG',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_protein': gene_myc_hs['@id']
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
            'tagged_protein': gene_myc_hs['@id']
        }
    )
    res = testapp.get(crispr_modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpRY-ANTI-FLAG fused to MYC'
