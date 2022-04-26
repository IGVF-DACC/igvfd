import pytest


@pytest.fixture
def organoid(testapp, lab, award, source):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'source': source['@id']
    }
<<<<<<< HEAD
    return testapp.post_json('/organoid', item, status=201).json['@graph'][0]
=======
    return testapp.post_json('/cell_line', item, status=201).json['@graph'][0]
>>>>>>> b4a3697 (added organoid)
