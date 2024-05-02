import pytest


@pytest.fixture
def orf_foxp(testapp, gene_myc_hs, award, other_lab):
    item = {
        'orf_id': 'CCSBORF1234',
        'gene': [
            gene_myc_hs['@id']
        ],
        'protein_id': 'ENSP00000001146.2',
        'dbxrefs': [
            'hORFeome:8945'
        ],
        'award': award['@id'],
        'lab': other_lab['@id'],
        'pct_identical_protein': 34,
        'pct_coverage_protein': 50,
        'pct_coverage_orf': 50
    }
    return testapp.post_json('/open_reading_frame', item, status=201).json['@graph'][0]


@pytest.fixture
def orf_zscan10(testapp, gene_zscan10_mm, award, other_lab):
    item = {
        'orf_id': 'CCSBORF4767',
        'gene': [
            gene_zscan10_mm['@id']
        ],
        'protein_id': 'ENSP00000317668',
        'dbxrefs': [
            'hORFeome:8947'
        ],
        'award': award['@id'],
        'lab': other_lab['@id'],
        'pct_identical_protein': 64,
        'pct_coverage_protein': 70,
        'pct_coverage_orf': 60
    }
    return testapp.post_json('/open_reading_frame', item, status=201).json['@graph'][0]


@pytest.fixture
def open_reading_frame_v1(orf_zscan10):
    item = orf_zscan10.copy()
    item.pop('award', None)
    item.pop('lab', None)
    item.update({
        'schema_version': '1',
    })
    return item
