import time

import pytest

from igvfd.commands import profile_render


def test_add_query_sets_and_overrides_params():
    assert profile_render.add_query(
        '/a/@@index-data-external?x=1', datastore='database', batch_embed='true'
    ) == '/a/@@index-data-external?x=1&datastore=database&batch_embed=true'
    assert profile_render.add_query('/a/?batch_embed=false', batch_embed='true') == '/a/?batch_embed=true'
    assert profile_render.add_query('/a/', datastore=None) == '/a/'


def test_parse_x_stats_converts_numbers_only():
    stats = profile_render.parse_x_stats('db_count=602&item_type=analysis_set&wsgi_time=509272')
    assert stats == {'db_count': 602.0, 'item_type': 'analysis_set', 'wsgi_time': 509272.0}


@pytest.mark.parametrize('path,expected', [
    ('/sequence-files/F0/@@object?skip_calculated=true', ('sequence-files', '@@object?skip_calculated')),
    ('/files/F0/@@object_with_select_calculated_properties?field=a&field=b',
     ('files', '@@object_with_select_calculated_properties?field')),
    ('/files/F0/@@filtered_object?include=a&exclude=b', ('files', '@@filtered_object?exclude&include')),
    ('/files/F0@@embedded', ('files', '@@embedded')),
])
def test_frame_key(path, expected):
    assert profile_render.frame_key(path) == expected


def test_frame_key_flags_frameless_embeds():
    assert profile_render.frame_key('/files/F0/')[1].startswith('(no frame')


def test_item_key_ignores_frame_and_query():
    assert profile_render.item_key('/files/F0/@@object?skip_calculated=true') == '/files/F0/'
    assert profile_render.item_key('/files/F0/') == '/files/F0/'


@pytest.mark.parametrize('filename,funcname,expected', [
    ('/igvfd/src/igvfd/audit/file_set.py', 'f', 'igvfd audits'),
    ('/igvfd/src/igvfd/types/file_set.py', 'f', 'igvfd types (calculated props)'),
    ('/usr/local/lib/python3.12/site-packages/snovault/embed.py', 'f', 'snovault'),
    ('/usr/local/lib/python3.12/site-packages/pyramid/router.py', 'f', 'pyramid / webob / zope'),
    ('/usr/local/lib/python3.12/site-packages/sqlalchemy/orm/query.py', 'f', 'sqlalchemy'),
    ('~', "<method 'execute' of 'psycopg2.extensions.cursor' objects>", 'database driver (psycopg2 wait)'),
    ('/usr/lib/python3.12/json/decoder.py', 'f', 'json / jsonschema'),
    ('/usr/lib/python3.12/copy.py', 'f', 'python builtins / stdlib / other'),
])
def test_category_of(filename, funcname, expected):
    assert profile_render.category_of(filename, funcname) == expected


def test_embed_tracer_splits_exclusive_from_inclusive_time(monkeypatch):
    import snovault.embed

    def fake_embed(request, path, as_user='EMBED'):
        time.sleep(0.01)
        if path.endswith('@@embedded'):
            snovault.embed._embed(None, '/files/F0/@@object?skip_calculated=true')
            snovault.embed._embed(None, '/files/F0/@@object?skip_calculated=true')
            snovault.embed._embed(None, '/files/F0/@@object', True)
        return {}

    monkeypatch.setattr(snovault.embed, '_embed', fake_embed)
    tracer = profile_render.EmbedTracer()
    tracer.install()
    try:
        snovault.embed._embed(None, '/file-sets/S/@@embedded')
    finally:
        tracer.remove()

    assert snovault.embed._embed is fake_embed
    assert tracer.total_renders == 4
    parent = tracer.records[('file-sets', '@@embedded')]
    child = tracer.records[('files', '@@object?skip_calculated')]
    assert parent['count'] == 1 and child['count'] == 2
    assert tracer.records[('files', '@@object')]['uncached'] == 1
    assert parent['inclusive'] >= parent['exclusive'] + child['inclusive']
    assert tracer.path_counts['/files/F0/@@object?skip_calculated=true'] == 2
    assert tracer.item_frames['/files/F0/'] == {'@@object?skip_calculated', '@@object'}


def test_summarize_sql_groups_bind_names_and_lists_tables():
    joined = (
        'SELECT resources.rid AS rid FROM resources '
        'LEFT OUTER JOIN current_propsheets AS cp ON resources.rid = cp.rid '
        'LEFT OUTER JOIN propsheets AS ps ON ps.sid = cp.sid WHERE resources.rid = %(param_1)s'
    )
    expected = 'SELECT resources, current_propsheets, propsheets WHERE resources.rid = ?'
    assert profile_render.summarize_sql(joined) == expected
    assert profile_render.summarize_sql(joined.replace('param_1', 'param_9')) == expected
    assert profile_render.summarize_sql('SELECT 1') == 'SELECT'


def test_sql_tracer_counts_statements_and_unregisters():
    from sqlalchemy import create_engine, event, text
    from sqlalchemy.engine import Engine
    engine = create_engine('sqlite://')
    tracer = profile_render.SqlTracer()
    tracer.install()
    try:
        with engine.connect() as connection:
            connection.execute(text('CREATE TABLE t (a INTEGER)'))
            for value in range(3):
                connection.execute(text('SELECT a FROM t WHERE a = :a'), {'a': value})
    finally:
        tracer.remove()
    assert tracer.total == 4
    assert max(tracer.counts.values()) == 3
    assert not event.contains(Engine, 'before_cursor_execute', tracer._before)


def test_print_audit_checkers_lists_only_igvfd_audit_functions(capsys):
    import cProfile
    import pstats
    code = compile('def audit_a():\n    return sum(range(100000))\ndef audit_b():\n    return 1\n', '/igvfd/src/igvfd/audit/x.py', 'exec')
    namespace = {}
    exec(code, namespace)
    profile = cProfile.Profile()
    profile.enable()
    namespace['audit_a']()
    namespace['audit_b']()
    profile.disable()
    profile_render.print_audit_checkers(pstats.Stats(profile), 5)
    output = capsys.readouterr().out
    assert output.index('audit_a') < output.index('audit_b')
    assert 'sum' not in output


@pytest.mark.parametrize('parameters,expected', [
    ({'name': 'accession', 'value': 'IGVFFI0001ABCD'}, ('accession', 'IGVFFI0001ABCD')),
    ({'name_1': 'alias', 'value_1': 'igvf:x'}, ('alias', 'igvf:x')),
    (('accession', 'IGVFFI0001ABCD'), ('accession', 'IGVFFI0001ABCD')),
    (None, ('?', '?')),
])
def test_key_lookup_params(parameters, expected):
    assert profile_render.key_lookup_params(parameters) == expected


def test_print_callers_of_lists_callers_by_call_count(capsys):
    import cProfile
    import pstats
    code = compile(
        'def target():\n    return 1\n'
        'def busy():\n    for _ in range(5):\n        target()\n'
        'def rare():\n    target()\n',
        '/igvfd/src/igvfd/audit/y.py', 'exec',
    )
    namespace = {}
    exec(code, namespace)
    profile = cProfile.Profile()
    profile.enable()
    namespace['busy']()
    namespace['rare']()
    profile.disable()
    profile_render.print_callers_of(pstats.Stats(profile), ('target',), 5)
    output = capsys.readouterr().out
    assert output.index('busy') < output.index('rare')


def test_find_differences_reports_paths_and_ignores_list_order():
    left = {'a': [1, 2, {'x': 1}], 'b': 'same', 'c': {'d': [3, 4]}}
    reordered = {'a': [{'x': 1}, 2, 1], 'b': 'same', 'c': {'d': [4, 3]}}
    normalize = profile_render.normalize_json
    assert profile_render.find_differences(normalize(left), normalize(reordered)) == []
    changed = {'a': [1, 2, {'x': 9}], 'b': 'same', 'c': {'d': [3, 4], 'e': 1}}
    paths = [path for path, _, _ in profile_render.find_differences(normalize(left), normalize(changed))]
    assert any(path.startswith('$.a') for path in paths)
    assert '$.c.e' in paths


def test_print_body_comparison_distinguishes_identical_reordered_and_different(capsys):
    def report(left, right):
        profile_render.print_body_comparison({'false': (None, None, None, left), 'true': (None, None, None, right)})
        return capsys.readouterr().out
    assert 'identical, including list order' in report({'a': [1, 2], 'xmin': 1}, {'a': [1, 2], 'xmin': 2})
    assert 'only the order' in report({'a': [1, 2]}, {'a': [2, 1]})
    output = report({'a': [1, 2]}, {'a': [1, 3]})
    assert 'DIFFER' in output and '$.a' in output
