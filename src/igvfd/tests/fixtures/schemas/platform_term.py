import pytest


@pytest.fixture
def platform_term_HiSeq(testapp):
    item = {
        'term_id': 'EFO:0004203',
        'term_name': 'Illumina HiSeq 2000'
    }
    return testapp.post_json('/platform_term', item, status=201).json['@graph'][0]


@pytest.fixture
def platform_term_NovaSeq(testapp):
    item = {
        'term_id': 'EFO:0008637',
        'term_name': 'Illumina NovaSeq 6000',
        'sequencing_kits': ['NovaSeq 6000 SP Reagent Kit v1.5',
                            'NovaSeq 6000 S1 Reagent Kit v1.5',
                            'NovaSeq 6000 S2 Reagent Kit v1.5',
                            'NovaSeq 6000 S4 Reagent Kit V1.5']
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
