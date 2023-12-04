import pytest


@pytest.fixture
def platform_term_HiSeq(testapp):
    item = {
        'term_id': 'EFO:0004203',
        'term_name': 'Illumina HiSeq 2000'
    }
    return testapp.post_json('/platform_term', item, status=201).json['@graph'][0]


@pytest.fixture
def platform_term_v1(platform_term_HiSeq):
    item = platform_term_HiSeq.copy()
    item.update({
        'schema_version': '1',
        'description': ''
    })
    return item
