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


@pytest.fixture
def software_version_v1(software_version):
    item = software_version.copy()
    item.update({
        'schema_version': '1',
        'references': ['10.1101/2023.08.02']
    })
    return item


@pytest.fixture
def software_version_v2(software_version):
    item = software_version.copy()
    item.update({
        'schema_version': '2',
        'version': '2.4.4.5',
    })
    return item


@pytest.fixture
def software_version_v2_no_v(software_version):
    item = software_version.copy()
    item.update({
        'schema_version': '2',
        'version': '2.4.4.5',
    })
    return item
