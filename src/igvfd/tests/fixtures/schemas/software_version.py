import pytest


@pytest.fixture
def software_version(testapp, software, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'software': software['@id'],
        'version': '2.4.4',
        'downloaded_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/'
    }
    return testapp.post_json('/software_version', item, status=201).json['@graph'][0]
