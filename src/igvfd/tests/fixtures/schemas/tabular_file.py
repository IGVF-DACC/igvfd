import pytest


@pytest.fixture
def tabular_file(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '01b08bb5485ac730df19af55ba4bb09c',
        'file_format': 'tsv',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'peaks',
        'controlled_access': False
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_onlist_1(testapp, lab, award, curated_set_barcode):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'b262f3f0ee029725169a63e0dcfb9b3b',
        'file_format': 'tsv',
        'file_set': curated_set_barcode['@id'],
        'content_type': 'barcode onlist',
        'controlled_access': False
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_onlist_2(testapp, lab, award, curated_set_barcode):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '4de470e4b4a86b9a57aa3cc8820f4d33',
        'file_format': 'tsv',
        'file_set': curated_set_barcode['@id'],
        'content_type': 'barcode onlist',
        'controlled_access': False
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_barcode_replacement(testapp, lab, award, curated_set_barcode):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '851086f8543eb2aff3488e82b25d45eb',
        'file_format': 'tsv',
        'file_set': curated_set_barcode['@id'],
        'content_type': 'barcode replacement',
        'controlled_access': False
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_bed(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '1897bf4e87141798373aced2a6508c28',
        'file_format_type': 'bed5',
        'file_format': 'bed',
        'assembly': 'GRCh38',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'peaks',
        'controlled_access': False
    }
    return testapp.post_json('/tabular_file', item, status=201).json['@graph'][0]


@pytest.fixture
def tabular_file_v1(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '1',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def tabular_file_v2(tabular_file_v1):
    item = tabular_file_v1.copy()
    item.update({
        'schema_version': '2',
        'description': ''
    })
    return item


@pytest.fixture
def tabular_file_v3(tabular_file_v1):
    item = tabular_file_v1.copy()
    item.update({
        'schema_version': '3',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def tabular_file_v4(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '069b0ebb6c5730dfe1d485acaf53b09c',
        'file_format': 'bed',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'peaks',
        'schema_version': '4'
    }
    return item


@pytest.fixture
def tabular_file_v5(tabular_file):
    item = tabular_file.copy()
    item.update({
        'assembly': 'hg19',
        'schema_version': '5'
    })
    return item


@pytest.fixture
def tabular_file_v7(tabular_file):
    item = tabular_file.copy()
    item.update({
        'derived_from': [],
        'file_format_specifications': [],
        'schema_version': '7'
    })
    return item


@pytest.fixture
def tabular_file_v10(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '10',
        'content_type': 'fold over change control'
    })
    return item


@pytest.fixture
def tabular_file_v11(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '11',
        'content_type': 'SNP effect matrix'
    })
    return item


@pytest.fixture
def tabular_file_v12(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '12',
        'file_format': 'txt'
    })
    return item


@pytest.fixture
def tabular_file_v14(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '14',
        'content_type': 'sequence barcodes'
    })
    return item


@pytest.fixture
def tabular_file_v16_1(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '16',
        'content_type': 'variant functional predictions'
    })
    return item


@pytest.fixture
def tabular_file_v16_2(tabular_file):
    item = tabular_file.copy()
    item.update({
        'schema_version': '16',
        'content_type': 'element to gene predictions'
    })
    return item
