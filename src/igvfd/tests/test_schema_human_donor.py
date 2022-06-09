import pytest


def test_accession(human_donor, testapp):
    res = testapp.get(human_donor['@id'])
    assert(res.json['accession'][:6] == 'IGVFDO')


def test_ethnicity(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicity': ['European']})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicity': ['Elf']}, expect_errors=True)
    assert(res.status_code == 422)


def test_fail_donor_with_three_parents(human_donor, parent_human_donor_1, parent_human_donor_2, parent_human_donor_3, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_human_donor_2['@id'],
            parent_human_donor_3['@id']
        ]}, expect_errors=True)
    assert(res.status_code == 422)


def test_fail_human_donor_with_rodent_parent(human_donor, parent_rodent_donor1, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_rodent_donor1['@id']
        ]}, expect_errors=True)
    assert(res.status_code == 422)


def test_fail_human_donor_with_human_and_rodent_parents(human_donor, parent_human_donor_1, parent_rodent_donor1, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [
            parent_human_donor_1['@id'],
            parent_rodent_donor1['@id']
        ]}, expect_errors=True)
    assert(res.status_code == 422)


def test_collections(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['ENCODE']})
    assert(res.status_code == 200)


def test_collections_fail(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['Something not collection']}, expect_errors=True)
    assert(res.status_code == 422)


def test_external_resources(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'external_resources': [
            {
                'resource_name': "Ig VH=immunoglobulin heavy chain variable region {VDJ rearrangement} [human, Richter's syndrome CLL patient 2, sample 1, Genomic Mutant, 112 nt]",
                'resource_identifier': 'GenBank: S69760.1',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        human_donor['@id'],
        {'external_resources': [
            {
                'resource_name': 'I am an external resource name.',
                'resource_identifier': 'I am an external resource identifier.'
            }
        ]})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        human_donor['@id'],
        {'external_resources': [
            {
                'resource_name': "Ig VH=immunoglobulin heavy chain variable region {VDJ rearrangement} [human, Richter's syndrome CLL patient 2, sample 1, Genomic Mutant, 112 nt]",
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        human_donor['@id'],
        {'external_resources': [
            {
                'resource_identifier': 'GenBank: S69760.1',
                'resource_url': 'https://www.ncbi.nlm.nih.gov/nuccore/S69760.1'
            }
        ]}, expect_errors=True)
    assert(res.status_code == 422)


def test_organism(award, lab, testapp):
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'organism': 'Homo sapiens'
        })
    assert(res.status_code == 201)
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'organism': 'Mus musculus'
        }, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.post_json(
        '/human_donor',
        {
            'award': award['@id'],
            'lab': lab['@id'],
            'organism': 'Saccharomyces'
        }, expect_errors=True)
    assert(res.status_code == 422)
