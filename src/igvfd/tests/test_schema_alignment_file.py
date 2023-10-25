import pytest


# This tests the regex that disallows submission of any pattern. Remove this test once dbxrefs are added for alignment files.
def test_restricted_dbxrefs(testapp, alignment_file):
    testapp.patch_json(
        alignment_file['@id'],
        {'dbxrefs': ['']}, expect_errors=True)
