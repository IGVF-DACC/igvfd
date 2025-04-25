import pytest


def test_audit_inconsistent_taxa(
    testapp,
    curated_set_genome,
    curated_set_transcriptome,
    human_donor,
    in_vitro_cell_line
):
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'taxa': 'Homo sapiens',
            'samples': [in_vitro_cell_line['@id']],
        }
    )
    res = testapp.get(curated_set_genome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent taxa'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        curated_set_transcriptome['@id'],
        {
            'taxa': 'Mus musculus',
            'donors': [human_donor['@id']]
        }
    )
    res = testapp.get(curated_set_genome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent taxa'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_non_virtual_sample(
    testapp,
    curated_set_transcriptome,
    in_vitro_cell_line
):
    testapp.patch_json(
        curated_set_transcriptome['@id'],
        {
            'samples': [in_vitro_cell_line['@id']],
        }
    )
    res = testapp.get(curated_set_transcriptome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )
    testapp.patch_json(
        in_vitro_cell_line['@id'],
        {
            'virtual': True
        }
    )
    res = testapp.get(curated_set_transcriptome['@id'] + '@@audit')
    assert all(
        error['category'] != 'inconsistent samples'
        for error in res.json['audit'].get('ERROR', [])
    )
