import pytest


def test_accession(rodent_donor, testapp):
    res = testapp.get(rodent_donor['@id'])
    assert(res.json['accession'][:6] == 'IGVFDO')


def test_lot_id_dependency(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert(res.status_code == 422)


def test_strain(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'strains': [{'strain_background': 'C57BL/6J (B6)', 'strain_name': 'B6.129P2-Tcrbtm1Mom/J', 'genotype': 'Some Genotype'}]})
    assert(res.status_code == 200)


def test_donor_with_three_parents(rodent_donor, parent_rodent_donor1, parent_rodent_donor2, parent_rodent_donor3, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [parent_rodent_donor1['@id'], parent_rodent_donor2['@id'], parent_rodent_donor3['@id']]})
    assert(res.status_code == 200)


def test_donor_with_no_parents(rodent_donor_orphan, testapp):
    res = testapp.patch_json(
        rodent_donor_orphan['@id'],
        {'parents': []})
    assert(res.status_code == 200)
