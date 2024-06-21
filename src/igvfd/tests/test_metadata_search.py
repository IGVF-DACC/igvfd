import pytest


def test_metadata_search_batched_search_generator_init(dummy_request):
    from igvfd.metadata.search import BatchedSearchGenerator
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    bsg = BatchedSearchGenerator(dummy_request)
    assert isinstance(bsg, BatchedSearchGenerator)
    assert bsg.batch_field == '@id'
    assert bsg.batch_size == 5000
    assert bsg.param_list == {'type': ['Experiment']}
    assert bsg.batch_param_values == []


def test_metadata_search_batched_search_generator_make_batched_values_from_batch_param_values(dummy_request):
    from igvfd.metadata.search import BatchedSearchGenerator
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment'
    )
    bsg = BatchedSearchGenerator(dummy_request)
    assert list(bsg._make_batched_values_from_batch_param_values()) == []
    from igvfd.metadata.metadata import BatchedSearchGenerator
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&@id=/files/ENCFFABC123/'
        '&@id=/files/ENCFFABC345/&@id=/files/ENCFFABC567/'
        '&@id=/files/ENCFFABC789/&@id=/files/ENCFFDEF123/'
        '&@id=/files/ENCFFDEF345/&@id=/files/ENCFFDEF567/'
    )
    bsg = BatchedSearchGenerator(dummy_request, batch_size=2)
    assert list(bsg._make_batched_values_from_batch_param_values()) == [
        ['/files/ENCFFABC123/', '/files/ENCFFABC345/'],
        ['/files/ENCFFABC567/', '/files/ENCFFABC789/'],
        ['/files/ENCFFDEF123/', '/files/ENCFFDEF345/'],
        ['/files/ENCFFDEF567/']
    ]
    bsg = BatchedSearchGenerator(dummy_request, batch_field='accession', batch_size=2)
    assert list(bsg._make_batched_values_from_batch_param_values()) == []
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&@id=/files/ENCFFABC123/'
        '&@id=/files/ENCFFABC345/&@id=/files/ENCFFABC567/'
        '&@id=/files/ENCFFABC789/&@id=/files/ENCFFDEF123/'
        '&@id=/files/ENCFFDEF345/&@id=/files/ENCFFDEF567/'
        '&accession=ENCFFAAA111'
    )
    bsg = BatchedSearchGenerator(dummy_request, batch_field='accession')
    assert next(bsg._make_batched_values_from_batch_param_values()) == ['ENCFFAAA111']


def test_metadata_search_batched_search_generator_make_batched_params_from_batched_values(dummy_request):
    from igvfd.metadata.search import BatchedSearchGenerator
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&@id=/files/ENCFFABC123/'
        '&@id=/files/ENCFFABC345/&@id=/files/ENCFFABC567/'
        '&@id=/files/ENCFFABC789/&@id=/files/ENCFFDEF123/'
        '&@id=/files/ENCFFDEF345/&@id=/files/ENCFFDEF567/'
    )
    bsg = BatchedSearchGenerator(dummy_request, batch_size=2)
    actual_batched_params = []
    for batched_values in bsg._make_batched_values_from_batch_param_values():
        actual_batched_params.append(
            bsg._make_batched_params_from_batched_values(batched_values)
        )
    expected_batched_params = [
        [('@id', '/files/ENCFFABC123/'), ('@id', '/files/ENCFFABC345/')],
        [('@id', '/files/ENCFFABC567/'), ('@id', '/files/ENCFFABC789/')],
        [('@id', '/files/ENCFFDEF123/'), ('@id', '/files/ENCFFDEF345/')],
        [('@id', '/files/ENCFFDEF567/')]
    ]
    assert expected_batched_params == actual_batched_params


def test_metadata_search_batched_search_generator_build_new_request(dummy_request):
    from igvfd.metadata.search import BatchedSearchGenerator
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&@id=/files/ENCFFABC123/'
        '&@id=/files/ENCFFABC345/&@id=/files/ENCFFABC567/'
        '&@id=/files/ENCFFABC789/&@id=/files/ENCFFDEF123/'
        '&@id=/files/ENCFFDEF345/&@id=/files/ENCFFDEF567/'
    )
    bsg = BatchedSearchGenerator(dummy_request, batch_size=2)
    batched_params = [('@id', '/files/ENCFFABC123/'), ('@id', '/files/ENCFFABC345/')]
    request = bsg._build_new_request(batched_params)
    assert str(request.query_string) == (
        'type=Experiment'
        '&%40id=%2Ffiles%2FENCFFABC123%2F'
        '&%40id=%2Ffiles%2FENCFFABC345%2F'
        '&limit=all'
    )
    assert request.path_info == '/search/'
    assert request.registry
    dummy_request.environ['QUERY_STRING'] = (
        'type=Experiment&@id=/files/ENCFFABC123/'
        '&@id=/files/ENCFFABC345/&@id=/files/ENCFFABC567/'
        '&@id=/files/ENCFFABC789/&@id=/files/ENCFFDEF123/'
        '&@id=/files/ENCFFDEF345/&@id=/files/ENCFFDEF567/'
        '&field=accession&files.status=released'
    )
    bsg = BatchedSearchGenerator(dummy_request, batch_size=2)
    batched_params = [('@id', '/files/ENCFFABC123/'), ('@id', '/files/ENCFFABC345/')]
    request = bsg._build_new_request(batched_params)
    assert request.query_string == (
        'type=Experiment&field=accession&files.status=released'
        '&%40id=%2Ffiles%2FENCFFABC123%2F'
        '&%40id=%2Ffiles%2FENCFFABC345%2F'
        '&limit=all'
    )
    assert request.path_info == '/search/'
    assert request.registry
