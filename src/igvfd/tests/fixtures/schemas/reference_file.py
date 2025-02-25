import pytest


@pytest.fixture
def reference_file(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7f1987dea86105dd9d2582c0a91c3156',
        'file_format': 'gtf',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'transcriptome reference',
        'controlled_access': False
    }
    return testapp.post_json('/reference_file', item, status=201).json['@graph'][0]


@pytest.fixture
def reference_file_two(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7f1987dea86105dd9d2582c0a91c1111',
        'file_format': 'gtf',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'transcriptome reference',
        'controlled_access': False
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


@pytest.fixture
def ref_file_v3(reference_file):
    item = reference_file.copy()
    item.update({
        'schema_version': '3',
        'transcriptome_annotation': 'V40'
    })
    return item


@pytest.fixture
def reference_file_v4(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '7d258f1987e2da2491ddb051a91c3156',
        'file_format': 'bed',
        'assembly': 'GRCh38',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'regulatory_regions'
    }
    return item


@pytest.fixture
def reference_file_v5(reference_file):
    item = reference_file.copy()
    item.update({
        'schema_version': '5',
        'dbxrefs': ['']
    })
    return item


@pytest.fixture
def reference_file_v6(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': 'fa751ddb77da240287e29051b863888b',
        'file_format': 'bed',
        'assembly': 'GRCh38',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'regulatory_regions',
        'schema_version': '6'
    }
    return item


@pytest.fixture
def reference_file_v7(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '7',
        'description': ''
    })
    return item


@pytest.fixture
def reference_file_v8(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '8',
        'upload_status': 'pending',
        'status': 'released'
    })
    return item


@pytest.fixture
def reference_file_v9(testapp, lab, award, principal_analysis_set):
    item = {
        'award': award['@id'],
        'lab': lab['@id'],
        'md5sum': '02c177dab4905127dfb77f9ef8a0648b',
        'file_format': 'bed',
        'file_set': principal_analysis_set['@id'],
        'content_type': 'regulatory_regions',
        'schema_version': '9'
    }
    return item


@pytest.fixture
def reference_file_v11(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '11',
        'derived_from': [],
        'file_format_specifications': []
    })
    return item


@pytest.fixture
def reference_file_v13(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '13',
        'status': 'in progress',
        'controlled_access': False,
        'upload_status': 'validated'
    })
    return item


@pytest.fixture
def reference_file_v14(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '14',
        'external': True,
        'external_id': 'ENCFF743WOO'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_genes(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_genes'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_genes_biosamples(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_genes_biosamples'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_genes_biosamples_donors(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_genes_biosamples_donors'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_genes_biosamples_treatments_chebi(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_genes_biosamples_treatments_chebi'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_genes_biosamples_treatments_proteins(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_genes_biosamples_treatments_proteins'
    })
    return item


@pytest.fixture
def reference_file_v15_regulatory_regions_regulatory_regions(reference_file_v6):
    item = reference_file_v6.copy()
    item.update({
        'schema_version': '15',
        'content_type': 'regulatory_regions_regulatory_regions'
    })
    return item
