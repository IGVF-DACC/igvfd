import pytest


@pytest.fixture
def software(testapp, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'title': 'Bowtie2',
        'name': 'bowtie2',
        'description': 'Bowtie 2 is an ultrafast and memory-efficient tool '
                       'aligning sequence reads to long reference sequences.',
        'source_url': 'https://bowtie-bio.sourceforge.net/bowtie2/index.shtml'
    }
    return testapp.post_json('/software', item, status=201).json['@graph'][0]


@pytest.fixture
def software_v1(software):
    item = software.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def software_v2(software_v1):
    item = software_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item
