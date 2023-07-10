import pytest


@pytest.fixture
def reference_file(testapp, lab, award, analysis_set_with_sample):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7f1987dea86105dd9d2582c0a91c3156',
        'file_format': 'gtf',
        'file_set': analysis_set_with_sample['@id'],
        'content_type': 'transcriptome reference'
    }
    return testapp.post_json('/reference_file', item, status=201).json['@graph'][0]


@pytest.fixture
def reference_file_v2(reference_file):
    item = reference_file.copy()
    item.update({
        'schema_version': '2',
        'source': 'foo://example.com:8042/over/there?name=ferret#nose'
     })
    return item


def ref_file_v3(reference_file):
    item = reference_file.copy()
    item.update({
        'schema_version': '3',
        'transcriptome_annotation': 'V40'
    })
    return item
