import pytest


def test_accession(rodent_donor, testapp):
    res = testapp.get(rodent_donor['@id'])
    assert res.json['accession'][:6] == 'IGVFDO'


def test_lot_id_dependency_success(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002', 'product_id': 'UberMouse5000'})
    assert res.status_code == 200


def test_lot_id_dependency_fail(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'lot_id': 'R00002'}, expect_errors=True)
    assert res.status_code == 422


def test_strain(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {
            'strain_background': 'C57BL/6J (B6)',
            'strain': 'B6.129P2-Tcrbtm1Mom/J',
            'genotype': 'Some Genotype'
        })
    assert res.status_code == 200


def test_fail_donor_with_three_parents(rodent_donor, parent_rodent_donor1, parent_rodent_donor2, parent_rodent_donor3, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_rodent_donor1['@id'],
            parent_rodent_donor2['@id'],
            parent_rodent_donor3['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_rodent_donor_with_human_parents(rodent_donor, parent_human_donor_1, parent_human_donor_2, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_fail_rodent_donor_with_rodent_and_human_parents(rodent_donor, parent_rodent_donor1, parent_human_donor_2, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'parents': [
            parent_rodent_donor1['@id'],
            parent_human_donor_2['@id']
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_collections(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'collections': [
            'ENCODE'
        ]})
    assert res.status_code == 200


def test_collections_fail(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'collections': [
            'I am the very model of a modern major-general.'
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_external_resources(rodent_donor, testapp):
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'external_resources': [
            {
                'resource_name': "Ig VH=immunoglobulin heavy chain variable region {VDJ rearrangement} [human, Richter's syndrome CLL patient 2, sample 1, Genomic Mutant, 112 nt]",
                'resource_identifier': 'GenBank: S69760.1',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]})
    assert res.status_code == 200
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'external_resources': [
            {
                'resource_name': 'I am an external resource name.',
                'resource_identifier': 'I am an external resource identifier.'
            }
        ]})
    assert res.status_code == 200
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'external_resources': [
            {
                'resource_name': "Ig VH=immunoglobulin heavy chain variable region {VDJ rearrangement} [human, Richter's syndrome CLL patient 2, sample 1, Genomic Mutant, 112 nt]",
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]}, expect_errors=True)
    assert res.status_code == 422
    res = testapp.patch_json(
        rodent_donor['@id'],
        {'external_resources': [
            {
                'resource_identifier': 'GenBank: S69760.1',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]}, expect_errors=True)
    assert res.status_code == 422


def test_taxa(award, lab, testapp):
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Mus musculus',
            'sex': 'male',
            'strain': 'B6'
        })
    assert res.status_code == 201
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Homo sapiens',
            'sex': 'male',
            'strain': 'B6'
        }, expect_errors=True)
    assert res.status_code == 422
    res = testapp.post_json(
        '/rodent_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'taxa': 'Saccharomyces',
            'sex': 'male',
            'strain': 'B6'
        }, expect_errors=True)
    assert res.status_code == 422
