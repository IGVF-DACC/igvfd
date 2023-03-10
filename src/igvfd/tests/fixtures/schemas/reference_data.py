import pytest


@pytest.fixture
def reference_data(testapp, award, lab, attachment):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': attachment['md5sum'],
        'file_format': 'gtf',
        'file_set': 'igvf:analysis_set_1',
        'content_type': 'transcriptome reference',
        'assembly': 'GRCh38'
    }
    return item
