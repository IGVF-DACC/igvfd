import pytest


def test_modification_summary(testapp, modification, gene_myc_hs):
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPRi SpdCas9'

    testapp.patch_json(
        modification['@id'],
        {
            'modality': 'activation',
            'fused_domain': 'VP64'
        }
    )
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPRa SpdCas9-VP64'

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

    testapp.patch_json(
        modification['@id'],
        {
            'cas': 'SpG',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_protein': gene_myc_hs['@id']
        }
    )
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpG-ANTI-FLAG fused to MYC'

    testapp.patch_json(
        modification['@id'],
        {
            'cas': 'SpRY',
            'cas_species': 'Streptococcus pyogenes (Sp)',
            'modality': 'localizing',
            'fused_domain': 'ANTI-FLAG',
            'tagged_protein': gene_myc_hs['@id']
        }
    )
    res = testapp.get(modification['@id'])
    assert res.json.get('summary') == 'CRISPR localizing SpRY-ANTI-FLAG fused to MYC'


def test_biosamples_modified(testapp, in_vitro_system_v20, modification_prime_editing):
    testapp.patch_json(
        in_vitro_system_v20['@id'],
        {
            'modifications': [modification_prime_editing['@id']]
        }
    )
    res = testapp.get(modification_prime_editing['@id'])
    assert res.json.get('biosamples_modified', []) == [in_vitro_system_v20['@id']]
