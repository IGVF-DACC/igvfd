import pytest


pytestmark = [pytest.mark.indexing]


def test_metadata_batch_download_v2_get_search_results_generator(workbook, dummy_request):
    from types import GeneratorType
    from igvfd.metadata.metadata import MetadataReportV2
    dummy_request.environ['QUERY_STRING'] = (
        'type=FileSet'
    )
    mr = MetadataReportV2(dummy_request)
    mr._build_params()
    search_results = mr._get_search_results_generator()
    assert isinstance(search_results, GeneratorType)
    assert len(list(search_results)) >= 70


def test_metadata_batch_download_v2_generate_rows(workbook, dummy_request):
    from types import GeneratorType
    from igvfd.metadata.metadata import MetadataReportV2
    dummy_request.environ['QUERY_STRING'] = (
        'type=FileSet'
    )
    mr = MetadataReportV2(dummy_request)
    mr._initialize_report()
    mr._build_params()
    row_generator = mr._generate_rows()
    assert isinstance(row_generator, GeneratorType)
    results = list(row_generator)
    assert len(results) >= 100
    # First column always file URL.
    assert results[0].decode('utf-8').split('\t')[1] == 'File download URL'


def test_metadata_batch_download_v2_generate(workbook, dummy_request):
    from types import GeneratorType
    from igvfd.metadata.metadata import MetadataReportV2
    from pyramid.response import Response
    dummy_request.environ['QUERY_STRING'] = (
        'type=FileSet'
    )
    mr = MetadataReportV2(dummy_request)
    response = mr.generate()
    assert isinstance(response, Response)
    assert response.content_type == 'text/tsv'
    assert response.content_disposition == 'attachment; filename="file_metadata.tsv"'
    assert len(list(response.body)) >= 100


def test_metadata_batch_download_v2_view(workbook, testapp):
    r = testapp.get('/batch-download-v2/?type=FileSet')
    assert len(r.text.split('\n')) >= 100


def test_metadata_batch_download_v2_view_subtypes(workbook, testapp):
    r = testapp.get('/batch-download-v2/?type=AnalysisSet')
    assert len(r.text.split('\n')) >= 70
    r = testapp.get('/batch-download-v2/?type=MeasurementSet')
    assert len(r.text.split('\n')) >= 10


def test_metadata_file_batch_download_v2_view(workbook, testapp):
    r = testapp.get('/file-batch-download-v2/?type=File')
    assert len(r.text.split('\n')) >= 80
    r = testapp.get('/file-batch-download-v2/?type=TabularFile')
    assert len(r.text.split('\n')) >= 40


def test_metadata_batch_download_v2_contains_audit_values(workbook, testapp):
    r = testapp.get('/batch-download-v2/?type=FileSet')
    audit_values = [
        'missing nucleic acid delivery',
        'upload status not validated',
        'missing file format specifications',
        'missing derived from',
        'missing dbxrefs',
        'missing analysis step version',
        'unexpected input file set',
        'missing input file set',
    ]
    for value in audit_values:
        assert value in r.text, f'{value} not in metadata report'


def test_metadata_file_batch_download_v2_contains_audit_values(workbook, testapp):
    r = testapp.get('/file-batch-download-v2/?type=File')
    audit_values = [
        'missing file format specifications',
        'upload status not validated',
    ]
    for value in audit_values:
        assert value in r.text, f'{value} not in metadata report'


def test_metadata_batch_download_v2_contains_all_values(workbook, testapp):
    from pkg_resources import resource_filename
    r = testapp.get('/batch-download-v2/?type=FileSet')
    actual = sorted([tuple(x.split('\t')) for x in r.text.strip().split('\n')])
    assert len(actual) >= 100


def test_metadata_file_batch_download_v2_contains_all_values(workbook, testapp):
    from pkg_resources import resource_filename
    r = testapp.get('/file-batch-download-v2/?type=File')
    actual = sorted([tuple(x.split('\t')) for x in r.text.strip().split('\n')])
    assert len(actual) >= 100


def test_metadata_batch_download_v2_contains_all_values_inequality_filter_file_size(workbook, testapp):
    from pkg_resources import resource_filename
    r = testapp.get('/batch-download-v2/?type=FileSet&files.file_size=lt:1000')
    actual = sorted([tuple(x.split('\t')) for x in r.text.strip().split('\n')])
    assert len(actual) >= 4


def test_metadata_batch_download_v2_all_files_recursive(workbook, testapp):
    expected = {
        'files': [
            '/configuration-files/IGVFFI0000CONF/',
            '/index-files/IGVFFI0001CRAI/',
            '/index-files/IGVFFI0002BAIN/',
            '/reference-files/IGVFFI0001SQBZ/',
            '/reference-files/IGVFFI0001VARI/',
            '/reference-files/IGVFFI0039TRAN/',
            '/reference-files/IGVFFI0836NNBT/',
            '/reference-files/IGVFFI0865ETVT/',
            '/reference-files/IGVFFI0868FSXA/',
            '/reference-files/IGVFFI1234KLJH/',
            '/reference-files/IGVFFI1276BJRG/',
            '/reference-files/IGVFFI1530UZOX/',
            '/reference-files/IGVFFI4150KMRP/',
            '/reference-files/IGVFFI5471EAMF/',
            '/reference-files/IGVFFI5806YWFK/',
            '/reference-files/IGVFFI6426JKYC/',
            '/reference-files/IGVFFI6668JREP/',
            '/reference-files/IGVFFI6791GUEE/',
            '/reference-files/IGVFFI7115PAJX/',
            '/reference-files/IGVFFI8455GRSQ/',
            '/sequence-files/IGVFFI1165AJSO/',
            '/sequence-files/IGVFFI5555PODD/',
            '/signal-files/IGVFFI5344BASE/',
            '/tabular-files/IGVFFI0000CSVV/',
            '/tabular-files/IGVFFI0000ELEM/',
            '/tabular-files/IGVFFI0000SBRD/',
            '/tabular-files/IGVFFI0001SBRC/',
            '/tabular-files/IGVFFI5155WZID/',
            '/tabular-files/IGVFFI6621MLMF/',
            '/tabular-files/IGVFFI7099DPQN/',
            '/tabular-files/IGVFFI8932EGPR/',
            '/tabular-files/IGVFFI9822PRSQ/',
            '/tabular-files/IGVFFI9900PPIP/'
        ],
        'file_sets': [
            '/analysis-sets/IGVFDS0101PIPE/',
            '/analysis-sets/IGVFDS5300PRAN/',
            '/auxiliary-sets/IGVFDS0001AUXI/',
            '/construct-library-sets/IGVFDS5436ABCD/',
            '/measurement-sets/IGVFDS0000MSET/',
            '/measurement-sets/IGVFDS0987SHAR/',
            '/model-sets/IGVFDS4321MODL/',
            '/prediction-sets/IGVFDS5145PRED/'
        ]
    }
    r = testapp.get('/analysis-sets/IGVFDS0101PIPE/@@all-files?soft=true')
    for f in expected['files']:
        assert f in r.json['files']
    for fs in expected['file_sets']:
        assert fs in r.json['file_sets']
