import pytest


@pytest.fixture
def genome_browser_annotation_file(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb08c',
        'file_format': 'tabix',
        'assembly': 'GRCh38',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'peaks',
        'derived_from': [reference_file['@id']]
    }
    return testapp.post_json('/genome_browser_annotation_file', item, status=201).json['@graph'][0]


@pytest.fixture
def genome_browser_annotation_file_v1(genome_browser_annotation_file):
    item = genome_browser_annotation_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def genome_browser_annotation_file_v2(genome_browser_annotation_file_v1):
    item = genome_browser_annotation_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def genome_browser_annotation_file_v3(genome_browser_annotation_file_v1):
    item = genome_browser_annotation_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def genome_browser_annotation_file_v4(testapp, lab, award, analysis_set_with_sample, reference_file):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '00df1835ba4bb0301a4babc9af51b07c',
        'file_format': 'tabix',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'peaks',
        'derived_from': [reference_file['@id']],
        'schema_version': '4'
    }
    return item
