import pytest


def test_document_characterization_dependency(testapp, experimental_protocol_document):
    res = testapp.patch_json(
        experimental_protocol_document['@id'],
        {'document_type': 'characterization'}, expect_errors=True)
    assert(res.status_code == 422)
    res = testapp.patch_json(
        experimental_protocol_document['@id'],
        {'document_type': 'characterization',
         'characterization_method': 'FACS'}, expect_errors=False)
    assert(res.status_code == 200)
