import pytest


def get_batch_download_and_metadata_results(testapp, query_string):
    batch_download_results = testapp.get(
        '/batch_download/' + query_string
    ).text.strip().split('\n')
    metadata_results = testapp.get(
        '/metadata/' + query_string
    ).text.strip().split('\n')
    return batch_download_results, metadata_results


def test_metadata_batch_download_init_batch_download_mixin(dummy_request):
    from igvfd.metadata.batch_download import BatchDownloadMixin
    bdm = BatchDownloadMixin()
    assert isinstance(bdm, BatchDownloadMixin)


def test_metadata_batch_download_init_batch_download(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    assert isinstance(bd, BatchDownload)


def test_metadata_batch_download_should_add_json_elements_to_metadata_link(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived&files'
    )
    bd = BatchDownload(dummy_request)
    assert not bd._should_add_json_elements_to_metadata_link()
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    bd = BatchDownload(dummy_request)
    assert bd._should_add_json_elements_to_metadata_link()
    dummy_request.json = {'elements': []}
    bd = BatchDownload(dummy_request)
    assert not bd._should_add_json_elements_to_metadata_link()
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived&files'
    )
    dummy_request.json = {
        'elements': [
            '/experiments/ENCSR123ABC/',
            '/experiments/ENCSRDEF567/'
        ]
    }
    bd = BatchDownload(dummy_request)
    assert bd._should_add_json_elements_to_metadata_link()


def test_metadata_batch_download_maybe_add_json_elements_to_metadata_link(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    metadata_link = bd._maybe_add_json_elements_to_metadata_link('')
    assert metadata_link == ''
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    bd = BatchDownload(dummy_request)
    metadata_link = bd._maybe_add_json_elements_to_metadata_link('')
    assert metadata_link == (
        ' -X GET -H "Accept: text/tsv" -H '
        '"Content-Type: application/json" '
        '--data \'{"elements": ["/experiments/ENCSR123ABC/"]}\''
    )
    dummy_request.json = {'elements': []}
    bd = BatchDownload(dummy_request)
    metadata_link = bd._maybe_add_json_elements_to_metadata_link('')
    assert metadata_link == ''
    dummy_request.json = {
        'elements': [
            '/experiments/ENCSR123ABC/',
            '/experiments/ENCSRDEF567/'
        ]
    }
    bd = BatchDownload(dummy_request)
    metadata_link = bd._maybe_add_json_elements_to_metadata_link('')
    assert metadata_link == (
        ' -X GET -H "Accept: text/tsv" -H '
        '"Content-Type: application/json" '
        '--data \'{"elements": ["/experiments/ENCSR123ABC/", "/experiments/ENCSRDEF567/"]}\''
    )


def test_metadata_batch_download_get_metadata_link(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    metadata_link = bd._get_metadata_link()
    assert metadata_link == (
        '"http://localhost/metadata/?type=Experiment'
        '&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status%21=archived"'
    )
    dummy_request.json = {
        'elements': [
            '/experiments/ENCSR123ABC/',
            '/experiments/ENCSRDEF567/'
        ]
    }
    bd = BatchDownload(dummy_request)
    metadata_link = bd._get_metadata_link()
    assert metadata_link == (
        '"http://localhost/metadata/?type=Experiment'
        '&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status%21=archived"'
        ' -X GET -H "Accept: text/tsv" -H "Content-Type: application/json"'
        ' --data \'{"elements": ["/experiments/ENCSR123ABC/", "/experiments/ENCSRDEF567/"]}\''
    )


def test_metadata_batch_download_get_encoded_metadata_link_with_newline(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    metadata_link = bd._get_encoded_metadata_link_with_newline()
    assert metadata_link == (
        '"http://localhost/metadata/?type=Experiment'
        '&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status%21=archived"'
        '\n'
    ).encode('utf-8')
    dummy_request.json = {
        'elements': [
            '/experiments/ENCSR123ABC/',
            '/experiments/ENCSRDEF567/'
        ]
    }
    bd = BatchDownload(dummy_request)
    metadata_link = bd._get_encoded_metadata_link_with_newline()
    assert metadata_link == (
        '"http://localhost/metadata/?type=Experiment'
        '&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status%21=archived"'
        ' -X GET -H "Accept: text/tsv" -H "Content-Type: application/json"'
        ' --data \'{"elements": ["/experiments/ENCSR123ABC/", "/experiments/ENCSRDEF567/"]}\''
        '\n'
    ).encode('utf-8')


def test_metadata_batch_download_default_params(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    assert bd.DEFAULT_PARAMS == [
        ('limit', 'all'),
        ('field', 'files.@id'),
        ('field', 'files.href'),
        ('field', 'files.file_format'),
        ('field', 'files.file_format_type')
    ]


def test_metadata_batch_download_build_header(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    bd._build_header()
    assert bd.header == ['File download URL']


def test_metadata_batch_download_get_column_to_field_mapping(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    assert list(bd._get_column_to_fields_mapping().items()) == [
        ('File download URL', ['files.href'])
    ]


def test_metadata_batch_download_build_params(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    dummy_request.json = {'elements': ['/experiments/ENCSR123ABC/']}
    bd = BatchDownload(dummy_request)
    bd._build_params()
    assert len(bd.param_list['field']) == 4, f'{len(bd.param_list["field"])} not expected'
    assert len(bd.param_list['@id']) == 1


def test_metadata_batch_download_build_query_string(dummy_request):
    from igvfd.metadata.batch_download import BatchDownload
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
    )
    bd = BatchDownload(dummy_request)
    bd._initialize_report()
    bd._build_params()
    bd._build_query_string()
    bd.query_string.deduplicate()
    assert str(bd.query_string) == (
        'type=Experiment&files.file_format=bigWig'
        '&files.file_format=bam&limit=all&field=files.%40id'
        '&field=files.href&field=files.file_format'
        '&field=files.file_format_type'
    )
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&files.file_format=bigWig&files.file_format=bam'
        '&files.replicate.library.size_range=50-100'
        '&files.status!=archived'
    )
    bd = BatchDownload(dummy_request)
    bd._initialize_report()
    bd._build_params()
    bd._build_query_string()
    assert str(bd.query_string) == (
        'type=Experiment&files.file_format=bigWig'
        '&files.file_format=bam&files.replicate.library.size_range=50-100'
        '&files.status%21=archived'
        '&limit=all&field=files.%40id&field=files.href'
        '&field=files.file_format&field=files.file_format_type'
        '&field=files.href&field=files.file_format&field=files.file_format'
        '&field=files.replicate.library.size_range'
    )
