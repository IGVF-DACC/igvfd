import pytest


@pytest.fixture
<<<<<<< HEAD
<<<<<<< HEAD:src/igvfd/tests/fixtures/schemas/biosample.py
def biosample_1(testapp, other_lab, award, source):
=======
def cell_line_1(testapp, other_lab, award):
>>>>>>> c654056 (biosample as abstract, cell_line replacing concrete biosample in tests):src/igvfd/tests/fixtures/schemas/cell_line.py
=======
def cell_line(testapp, other_lab, award):
>>>>>>> b5fb316 (added tissue)
    item = {
        'award': award['@id'],
        'lab': other_lab['@id'],
        'source': other_lab['@id']
    }
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]
