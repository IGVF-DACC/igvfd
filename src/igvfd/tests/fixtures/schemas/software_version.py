import pytest


@pytest.fixture
def software_version(testapp, software, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'software': software['@id'],
        'version': 'v2.4.4',
        'source_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/'
    }
    return testapp.post_json('/software_version', item, status=201).json['@graph'][0]


@pytest.fixture
def software_version_with_download_id(testapp, software, lab, award):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'software': software['@id'],
        'version': 'v5.0.5.5',
        'download_id': 'd31294875092e76ebb061eadc7998585'
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
        'version': '2.4.4',
    })
    return item


@pytest.fixture
def software_version_v3(software_version_v2):
    item = software_version_v2.copy()
    item.update({
        'schema_version': '3',
        'description': '',
    })
    return item


@pytest.fixture
def software_version_v5(software_version):
    item = software_version.copy()
    item.update({
        'schema_version': '5',
        'publication_identifiers': ['doi:10.1016/j.molcel.2021.05.020']
    })
    return item


@pytest.fixture
def software_version_v6(software_version_with_download_id):
    item = software_version_with_download_id.copy()
    item.update({
        'schema_version': '6',
        'downloaded_url': 'https://sourceforge.net/projects/bowtie-bio/files/bowtie2/2.4.4/'
    })
    return item
