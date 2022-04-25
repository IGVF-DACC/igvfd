import pytest


def test_treatment_type_dependency(self, testapp){
    res = testapp.patch_json(
        treatment['@id'],
        {'treatment_type': 'chemical', 'treatment_id': 'CHEBI:24996'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment['@id'],
        {'treatment_type': 'protein', 'treatment_id': 'UniProtKB:P09919'})
    assert(res.status_code == 200)
    res = testapp.patch_json(
        treatment['@id'],
        {'treatment_type': 'chemical', 'treatment_id': 'UniProtKB:P09919'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        treatment['@id'],
        {'treatment_type': 'protein', 'treatment_id': 'CHEBI:24996'}, expect_errors=True)
    assert(res.status_code == 422)
}
