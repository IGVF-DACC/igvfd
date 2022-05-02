import pytest


def test_accession(human_donor, testapp):
    res = testapp.get(human_donor['@id'])
    assert(res.json['accession'][:6] == 'IGVFDO')


def test_health_status(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'health_status_history': [
            {
                'health_description': 'Subject displayed confusion and inebriation due to severe amounts of alcohol.',
                'date_start': '1999-12-30',
                'date_end': '2000-01-02'
            }
        ]})
    assert(res.status_code == 200)


def test_ethnicity(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicity': ['European']})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        human_donor['@id'],
        {'ethnicity': ['Elf']}, expect_errors=True)
    print('status code: ' + str(res.status_code))
    assert(res.status_code == 422)


def test_donor_with_parents(human_donor, parent_human_donor_1, parent_human_donor_2, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'parents': [parent_human_donor_1['@id'], parent_human_donor_2['@id']]})
    assert(res.status_code == 200)


def test_donor_with_no_parents(human_donor_orphan, testapp):
    res = testapp.patch_json(
        human_donor_orphan['@id'],
        {'parents': []})
    assert(res.status_code == 200)


def test_collections(human_donor, testapp):
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['ENCODE']})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        human_donor['@id'],
        {'collections': ['Something not collection']}, expect_errors=True)
    print('status code: ' + str(res.status_code))
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
