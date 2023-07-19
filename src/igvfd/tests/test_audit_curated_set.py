import pytest


def test_audit_donors_mismatch(
    testapp,
    curated_set_genome,
    human_donor,
    in_vitro_cell_line,
    in_vitro_differentiated_cell
):
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'samples': [in_vitro_cell_line['@id'], in_vitro_differentiated_cell['@id']],
            'donors': [human_donor['@id']]
        }
    )
    res = testapp.get(curated_set_genome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent donors metadata'
        for error in res.json['audit'].get('ERROR', [])
    )


def test_audit_related_multiome_datasets(
    testapp,
    curated_set_genome,
    human_donor,
    in_vitro_cell_line
):
    testapp.patch_json(
        curated_set_genome['@id'],
        {
            'taxa': 'Homo sapiens',
            'samples': [in_vitro_cell_line['@id']],
            'donors': [human_donor['@id']]
        }
    )
    res = testapp.get(curated_set_genome['@id'] + '@@audit')
    assert any(
        error['category'] == 'inconsistent taxa metadata'
        for error in res.json['audit'].get('ERROR', [])
    )
