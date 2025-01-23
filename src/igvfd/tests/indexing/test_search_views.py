import pytest


pytestmark = [pytest.mark.indexing]


def test_search_views_search_view_with_filters(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&lab=/labs/j-michael-cherry/'
    )
    assert r.json['title'] == 'Search'
    assert len(r.json['@graph']) >= 22
    r = testapp.get(
        '/search/?type=User&lab=/labs/j-michael-cherry/&title=Ben%20Hitz'
    )
    assert r.json['@graph'][0]['title'] == 'Ben Hitz'
    assert 'User' in r.json['@graph'][0]['@type']
    assert r.json['@id'] == '/search/?type=User&lab=/labs/j-michael-cherry/&title=Ben%20Hitz'
    assert r.json['@context'] == '/terms/'
    assert r.json['@type'] == ['Search']
    assert r.json['total'] == 1
    assert r.json['notification'] == 'Success'
    assert len(r.json['filters']) >= 2
    assert r.status_code == 200
    assert r.json['clear_filters'] == '/search/?type=User'
    assert 'debug' not in r.json
    assert 'columns' in r.json
    assert 'sort' in r.json


def test_search_views_search_view_with_limit(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&limit=5'
    )
    assert len(r.json['@graph']) == 5
    assert 'all' in r.json
    r = testapp.get(
        '/search/?type=User&limit=26'
    )
    assert len(r.json['@graph']) == 26
    assert 'all' in r.json
    r = testapp.get(
        '/search/?type=User&limit=all'
    )
    assert len(r.json['@graph']) >= 100
    assert 'all' not in r.json
    r = testapp.get(
        '/search/?type=User&limit=48'
    )
    assert len(r.json['@graph']) == 48
    r = testapp.get(
        '/search/?type=User&limit=100000'
    )
    assert len(r.json['@graph']) >= 100
    assert 'all' not in r.json


def test_search_views_search_view_with_limit_zero(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&limit=0'
    )
    assert len(r.json['@graph']) == 0
    assert 'all' in r.json
    assert r.json['total'] >= 48


def test_search_views_search_view_values(workbook, testapp):
    r = testapp.get(
        '/search/?status=released'
    )
    assert r.json['all'] == '/search/?status=released&limit=all'
    assert r.json['notification'] == 'Success'
    assert r.json['filters'][0] == {'field': 'status', 'remove': '/search/', 'term': 'released'}
    assert r.json['clear_filters'] == '/search/'


def test_search_views_search_view_values_no_results(workbook, testapp):
    r = testapp.get(
        '/search/?status=released&type=User',
        status=404
    )
    assert r.json['notification'] == 'No results found'


def test_search_views_search_view_values_malformed_query_string(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&status=&format=json',
        status=404
    )
    assert r.json['notification'] == 'No results found'


def test_search_views_search_view_values_bad_type(workbook, testapp):
    r = testapp.get(
        '/search/?status=released&type=Exp',
        status=400
    )
    assert r.json['description'] == "Invalid types: ['Exp']"
    r = testapp.get(
        '/search/?status=released&type=Exp&type=Per',
        status=400
    )
    assert r.json['description'] == "Invalid types: ['Exp', 'Per']"


def test_search_views_search_view_values_item_wildcard(workbook, testapp):
    r = testapp.get(
        '/search/?type=*',
    )
    assert r.json['notification'] == 'Success'
    assert r.json['total'] >= 300


def test_search_views_search_view_values_invalid_search_term(workbook, testapp):
    r = testapp.get(
        '/search/?query=[',
        status=404
    )


def test_search_views_search_view_values_invalid_advanced_query(workbook, testapp):
    r = testapp.get(
        '/search/?advancedQuery=[',
        status=400
    )
    assert r.json['description'] == 'Invalid query: ['


def test_search_views_search_view_embedded_frame(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&frame=embedded'
    )
    assert r.json['@graph'][0]['submits_for']


def test_search_views_search_view_object_frame(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&frame=object'
    )
    res = r.json['@graph'][0]
    assert all(
        [
            x in res
            for x in ['uuid', '@type', '@id', 'title']
        ]
    )


def test_search_views_search_view_debug_query(workbook, testapp):
    r = testapp.get(
        '/search/?type=User&debug=true'
    )
    assert 'debug' in r.json
    assert 'post_filter' in r.json['debug']['raw_query']


def test_search_views_search_view_no_type(workbook, testapp):
    r = testapp.get('/search/')
    assert 'total' in r.json
    assert 'filters' in r.json
    assert len(r.json['filters']) == 0


def test_search_views_search_view_no_type_debug(workbook, testapp):
    r = testapp.get('/search/?debug=true')
    assert not r.json['debug']['raw_query']['post_filter']['bool']


def test_search_views_search_generator(workbook, dummy_request, threadlocals):
    from types import GeneratorType
    dummy_request.environ['QUERY_STRING'] = (
        'type=*&limit=all'
    )
    from igvfd.searches.generator import search_generator
    r = search_generator(dummy_request)
    assert '@graph' in r
    assert len(r.keys()) == 1
    assert isinstance(r['@graph'], GeneratorType)
    hits = [dict(h) for h in r['@graph']]
    assert len(hits) >= 310
    assert '@id' in hits[0]


def test_search_views_search_generator_field_specified(workbook, dummy_request, threadlocals):
    from types import GeneratorType
    dummy_request.environ['QUERY_STRING'] = (
        'type=User&field=@id&limit=5'
    )
    from igvfd.searches.generator import search_generator
    r = search_generator(dummy_request)
    assert '@graph' in r
    assert len(r.keys()) == 1
    assert isinstance(r['@graph'], GeneratorType)
    hits = [dict(h) for h in r['@graph']]
    assert len(hits) == 5
    assert '@id' in hits[0]
    assert len(hits[0].keys()) == 2


def test_search_views_report_view(workbook, testapp):
    r = testapp.get(
        '/report/?type=Gene&symbol=BAP1&symbol=CXXC1'
    )
    assert r.json['title'] == 'Report'
    assert len(r.json['@graph']) == 2
    assert 'Gene' in r.json['@graph'][0]['@type']
    assert len(r.json['facets']) >= 2
    assert r.json['@id'] == '/report/?type=Gene&symbol=BAP1&symbol=CXXC1'
    assert r.json['@context'] == '/terms/'
    assert r.json['@type'] == ['Report']
    assert r.json['total'] == 2
    assert r.json['notification'] == 'Success'
    assert len(r.json['filters']) == 3
    assert r.status_code == 200
    assert r.json['clear_filters'] == '/report/?type=Gene'
    assert 'debug' not in r.json
    assert 'columns' in r.json
    assert len(r.json['columns']) >= 5
    assert 'non_sortable' in r.json
    assert 'sort' in r.json


def test_search_views_report_response_with_search_term_type_only_clear_filters(workbook, testapp):
    r = testapp.get(
        '/report/?query=cherry&type=Lab'
    )
    assert 'clear_filters' in r.json
    assert r.json['clear_filters'] == '/report/?type=Lab'


def test_search_views_report_view_with_limit(workbook, testapp):
    r = testapp.get(
        '/report/?type=User&limit=5'
    )
    assert len(r.json['@graph']) == 5
    assert 'all' in r.json
    r = testapp.get(
        '/report/?type=User&limit=26'
    )
    assert len(r.json['@graph']) == 26
    assert 'all' in r.json
    r = testapp.get(
        '/report/?type=User&limit=all'
    )
    assert len(r.json['@graph']) >= 48
    assert 'all' not in r.json
    r = testapp.get(
        '/report/?type=User&limit=48'
    )
    assert len(r.json['@graph']) == 48
    r = testapp.get(
        '/report/?type=User&limit=100000'
    )
    assert len(r.json['@graph']) >= 48


def test_search_views_report_view_with_limit_zero(workbook, testapp):
    r = testapp.get(
        '/report/?type=User&limit=0'
    )
    assert len(r.json['@graph']) == 0
    assert 'all' in r.json
    assert r.json['total'] >= 48


def test_search_views_report_view_with_limit_zero_from_zero(workbook, testapp):
    r = testapp.get(
        '/report/?type=User&limit=0&from=0'
    )
    assert len(r.json['@graph']) == 0
    assert 'all' in r.json
    assert r.json['total'] >= 48


def test_search_views_report_view_values_bad_type(workbook, testapp):
    r = testapp.get(
        '/report/?status=released&type=Exp',
        status=400
    )
    assert r.json['description'] == "Invalid types: ['Exp']"
    r = testapp.get(
        '/report/?status=released&type=Exp&type=Per',
        status=400
    )
    assert r.json['description'] == "Report view requires specifying a single type: [('type', 'Exp'), ('type', 'Per')]"


def test_search_views_report_view_values_single_subtype(workbook, testapp):
    r = testapp.get(
        '/report/?status=released&type=Item',
        status=400
    )
    assert 'Report view requires a type with no child types:' in r.json['description']


def test_search_views_report_view_values_no_type(workbook, testapp):
    r = testapp.get(
        '/report/?status=released',
        status=400
    )
    assert r.json['description'] == 'Report view requires specifying a single type: []'


def test_search_views_collection_listing_es_view(workbook, testapp):
    r = testapp.get(
        '/users/'
    )
    assert '@graph' in r.json
    assert '@id' in r.json
    assert 'facets' in r.json
    assert 'filters' in r.json
    assert 'all' in r.json
    assert 'columns' in r.json
    assert 'clear_filters' in r.json
    assert r.json['clear_filters'] == '/search/?type=User'
    assert r.json['@type'] == ['UserCollection', 'Collection']
    assert r.json['@context'] == '/terms/'


def test_search_views_collection_listing_es_view_item(workbook, testapp):
    r = testapp.get(
        '/User',
    )
    r = r.follow()
    assert '@graph' in r.json
    assert '@id' in r.json
    assert 'facets' in r.json
    assert 'filters' in r.json
    assert r.json['@type'] == ['UserCollection', 'Collection']
    assert r.json['@context'] == '/terms/'


def test_search_views_collection_listing_db_view(workbook, testapp):
    r = testapp.get(
        '/users/?datastore=database'
    )
    assert '@graph' in r.json
    assert '@id' in r.json
    assert 'facets' not in r.json
    assert 'filters' not in r.json
    assert r.json['@type'] == ['UserCollection', 'Collection']
    assert r.json['@context'] == '/terms/'
    assert r.json['description'] == 'Listing of current users'


def test_search_views_top_hits_raw_view(workbook, testapp):
    r = testapp.get(
        '/top-hits-raw/?query=CXX&field=@id'
    )
    assert 'aggregations' in r.json


def test_search_views_top_hits_view(workbook, testapp):
    r = testapp.get(
        '/top-hits/'
    )
    assert r.json['@type'] == ['TopHitsSearch']


def test_search_views_search_config_registry(workbook, testapp):
    r = testapp.get(
        '/search-config-registry/'
    )
    assert 'configs' in r.json
    assert 'defaults' in r.json
    assert 'aliases' in r.json
    configs = r.json['configs']
    assert len(configs) > 40
    assert 'User' in configs
    assert 'Award' in configs
    assert 'facets' in configs['Award']
    assert 'columns' in configs['Award']


def test_search_views_multireport_view_values(workbook, testapp):
    r = testapp.get(
        '/multireport/?status=released'
    )
    assert r.json['all'] == '/multireport/?status=released&limit=all'
    assert r.json['notification'] == 'Success'
    assert r.json['filters'][0] == {'field': 'status', 'remove': '/multireport/', 'term': 'released'}
    assert r.json['clear_filters'] == '/multireport/'


def test_search_views_search_quick(workbook, testapp):
    r = testapp.get(
        '/search-quick/?type=User&lab=/labs/j-michael-cherry/'
    )
    assert len(r.json['@graph']) >= 22


def test_search_views_dataset_summary(workbook, testapp):
    r = testapp.get(
        '/dataset-summary'
    )
    assert len(r.json['@graph']) >= 10


def test_search_views_dataset_summary_agg(workbook, testapp):
    testapp.get(
        '/dataset-summary-agg',
        status=400,
    )
    r = testapp.get(
        '/dataset-summary-agg?type=MeasurementSet&config=PreferredAssayTitleSummary',
        status=200,
    )
    assert 'matrix' in r.json
    assert r.json['matrix']['y']['doc_count'] > 10
    assert r.json['matrix']['y']['lab.title']['buckets'][0]['preferred_assay_title']['buckets'] is not None
    r = testapp.get(
        '/dataset-summary-agg?type=AnalysisSet&config=AssayTitlesSummary',
        status=200,
    )
    assert r.json['matrix']['y']['lab.title']['buckets'][0]['assay_titles']['buckets'][0]['status']['buckets'] is not None
    r = testapp.get(
        '/dataset-summary-agg?type=PredictionSet&config=FileSetTypeSummary',
        status=200,
    )
    assert r.json['matrix']['y']['lab.title']['buckets'][0]['file_set_type']['buckets'][0]['status']['buckets'] is not None


def test_search_views_datasets_released(workbook, testapp):
    r = testapp.get(
        '/datasets-released'
    )
    assert 'datasets_released' in r.json
    assert len(r.json['datasets_released']) >= 7
    assert any(
        'Mar 2024' in item
        for item in r.json['datasets_released']
    )
    assert list(r.json['datasets_released'][0].values())[0] > 20


def test_search_views_missing_matrix(workbook, testapp):
    r = testapp.get(
        '/missing-matrix?type=MeasurementSet&config=PreferredAssayTitleSummary'
    )
    assert r.json['total'] > 10
    assert 'matrix' in r.json
