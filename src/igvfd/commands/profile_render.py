"""Profile how igvfd renders a URL, optionally comparing snovault's batch_embed on and off.

Only issues GET requests. The source tree is mounted in the pyramid container, so no rebuild is needed:

    docker compose exec pyramid python -m igvfd.commands.profile_render \\
        config/pyramid/ini/development.ini \\
        /analysis-sets/IGVFDS5575ANST/@@index-data-external --username INDEXER

Per mode it reports median timings and SQL counts from the X-Stats header, how long
each layer (pyramid, sqlalchemy, igvfd types, audits, ...) spends in its own code, call counts for
the key snovault functions, and which (collection, frame) embeds are rendered most and
most often repeated. Profiled times are inflated by cProfile; compare shares, not seconds.
Pass --out DIR to save .prof files for snakeviz or pstats.
"""
import argparse
import collections
import json
import cProfile
import os
import pstats
import re
import statistics
import sys
import time
from urllib.parse import parse_qs, parse_qsl, urlencode, urlsplit, urlunsplit

KEY_FUNCTIONS = [
    ('request.embed calls', 'snovault/embed.py', 'embed'),
    ('subrequests rendered (_embed)', 'snovault/embed.py', '_embed'),
    ('pyramid invoke_subrequest', 'pyramid/router.py', 'invoke_subrequest'),
    ('item_links', 'snovault/resource_views.py', 'item_links'),
    ('uuid_to_path', 'snovault/resource_views.py', 'uuid_to_path'),
    ('calculate_properties', 'snovault/calculated.py', 'calculate_properties'),
    ('calculate_filtered_properties', 'snovault/calculated.py', 'calculate_filtered_properties'),
    ('upgrade_properties', 'snovault/resources.py', 'upgrade_properties'),
    ('quick_deepcopy (recursive)', 'snovault/util.py', 'quick_deepcopy'),
    ('Connection.get_by_uuid', 'snovault/connection.py', 'get_by_uuid'),
    ('Connection.get_by_uuids', 'snovault/connection.py', 'get_by_uuids'),
    ('Connection.get_by_unique_key', 'snovault/connection.py', 'get_by_unique_key'),
    ('Connection.warm_cache_for_paths', 'snovault/connection.py', 'warm_cache_for_paths'),
    ('Auditor.audit', 'snovault/auditor.py', 'audit'),
]

CATEGORIES = [
    ('igvfd audits', lambda rel, n: rel.startswith('igvfd/audit/')),
    ('igvfd types (calculated props)', lambda rel, n: rel.startswith('igvfd/types/')),
    ('igvfd other', lambda rel, n: rel.startswith('igvfd/')),
    ('snovault', lambda rel, n: rel.startswith('snovault/')),
    ('database driver (psycopg2 wait)', lambda rel, n: 'psycopg2' in rel or 'psycopg2' in n),
    ('sqlalchemy', lambda rel, n: rel.startswith('sqlalchemy/')),
    ('pyramid / webob / zope', lambda rel, n: rel.startswith(('pyramid/', 'webob/', 'zope/', 'venusian/'))),
    ('opensearch client', lambda rel, n: rel.startswith(('opensearchpy/', 'urllib3/'))),
    ('json / jsonschema', lambda rel, n: rel.startswith('jsonschema/') or '/json/' in rel),
]


def package_relative(filename):
    filename = filename.replace('\\', '/')
    for marker in ('/site-packages/', '/src/'):
        if marker in filename:
            return filename.split(marker, 1)[1]
    return filename


def add_query(path, **params):
    """Return path with params set, replacing any existing values and skipping None."""
    parts = urlsplit(path)
    query = dict(parse_qsl(parts.query))
    query.update({k: v for k, v in params.items() if v is not None})
    return urlunsplit(('', '', parts.path, urlencode(query), ''))


def parse_x_stats(header):
    stats = {}
    for key, values in parse_qs(header).items():
        try:
            stats[key] = float(values[0])
        except ValueError:
            stats[key] = values[0]
    return stats


def frame_key(path):
    """(collection, frame) for an embed path; query values are dropped, names kept."""
    base, _, query = path.partition('?')
    segments = [segment for segment in base.split('/') if segment]
    collection = segments[0] if segments else ''
    match = re.search(r'@@[\w-]+', base)
    label = match.group(0) if match else '(no frame: renders page, runs audit)'
    names = sorted(parse_qs(query))
    return collection, label + ('?' + '&'.join(names) if names else '')


def item_key(path):
    return path.partition('?')[0].split('@@')[0].rstrip('/') + '/'


def summarize_sql(statement):
    """Verb, tables and WHERE clause with bind names collapsed, so repeats group together."""
    text = ' '.join(statement.split())
    text = re.sub(r'%\(\w+\)s|\?|%s', '?', text)
    verb = text.split(' ', 1)[0].upper()
    tables = list(dict.fromkeys(re.findall(r'(?:FROM|JOIN|INTO|UPDATE)\s+([A-Za-z_][\w.]*)', text, re.IGNORECASE)))
    where = re.split(r'\bWHERE\b', text, maxsplit=1, flags=re.IGNORECASE)
    clause = where[1].strip()[:90] if len(where) > 1 else ''
    return (f'{verb} {", ".join(tables)}' + (f' WHERE {clause}' if clause else '')).strip()


def key_lookup_params(parameters):
    """(key name, value) from the bind parameters of a unique-key lookup."""
    if isinstance(parameters, dict):
        name = parameters.get('name', parameters.get('name_1'))
        value = parameters.get('value', parameters.get('value_1'))
        return str(name), str(value)
    values = list(parameters or ())
    return tuple(str(v) for v in (values + ['?', '?'])[:2])


def project_call_site(depth=6):
    """Nearest snovault/igvfd frames above the current call, innermost first."""
    frame = sys._getframe(2)
    sites = []
    while frame is not None and len(sites) < depth:
        filename = frame.f_code.co_filename.replace('\\', '/')
        if ('/snovault/' in filename or '/igvfd/' in filename) and 'profile_render' not in filename:
            sites.append(f'{os.path.basename(filename)}:{frame.f_code.co_name}')
        frame = frame.f_back
    return ' <- '.join(sites) or '(outside snovault/igvfd)'


class SqlTracer:
    """Counts executed SQL statements by summary and calling snovault/igvfd code."""

    def __init__(self):
        self.counts = collections.Counter()
        self.key_lookups = collections.Counter()

    def install(self):
        from sqlalchemy import event
        from sqlalchemy.engine import Engine
        self._event, self._engine = event, Engine
        event.listen(Engine, 'before_cursor_execute', self._before)

    def remove(self):
        self._event.remove(self._engine, 'before_cursor_execute', self._before)

    def _before(self, conn, cursor, statement, parameters, context, executemany):
        self.counts[(summarize_sql(statement), project_call_site())] += 1
        if 'keys.name' in statement and 'keys.value' in statement:
            self.key_lookups[key_lookup_params(parameters)] += 1

    @property
    def total(self):
        return sum(self.counts.values())


def category_of(filename, funcname):
    rel = package_relative(filename)
    for name, matches in CATEGORIES:
        if matches(rel, funcname):
            return name
    return 'python builtins / stdlib / other'


class EmbedTracer:
    """Wraps snovault.embed._embed to count subrequest renders and split inclusive from exclusive time."""

    def __init__(self):
        self.records = collections.defaultdict(
            lambda: {'count': 0, 'uncached': 0, 'inclusive': 0.0, 'exclusive': 0.0}
        )
        self.path_counts = collections.Counter()
        self.item_frames = collections.defaultdict(set)
        self._stack = []
        self._module = None
        self._original = None

    def install(self):
        import snovault.embed
        self._module = snovault.embed
        self._original = snovault.embed._embed
        snovault.embed._embed = self._traced

    def remove(self):
        if self._module is not None:
            self._module._embed = self._original

    def _traced(self, request, path, *args, **kwargs):
        frame = [time.perf_counter(), 0.0]
        self._stack.append(frame)
        try:
            return self._original(request, path, *args, **kwargs)
        finally:
            self._stack.pop()
            inclusive = time.perf_counter() - frame[0]
            if self._stack:
                self._stack[-1][1] += inclusive
            key = frame_key(path)
            record = self.records[key]
            record['count'] += 1
            record['uncached'] += 1 if (args or kwargs) else 0
            record['inclusive'] += inclusive
            record['exclusive'] += inclusive - frame[1]
            self.path_counts[path] += 1
            self.item_frames[item_key(path)].add(key[1])

    @property
    def total_renders(self):
        return sum(r['count'] for r in self.records.values())


def short_name(func_key):
    filename, lineno, funcname = func_key
    marker = 'site-packages/'
    if marker in filename:
        filename = filename.split(marker, 1)[1]
    elif '/src/' in filename:
        filename = filename.split('/src/', 1)[1]
    return f'{filename}:{lineno}({funcname})'


def find_function(stats, suffix, funcname):
    for (filename, _, name), values in stats.stats.items():
        if name == funcname and filename.replace('\\', '/').endswith(suffix):
            return values
    return None


def print_table(title, headers, rows):
    print(f'\n{title}')
    widths = [max(len(str(r[i])) for r in [headers] + rows) for i in range(len(headers))]
    print('  ' + '  '.join(str(h).ljust(w) if i == 0 else str(h).rjust(w) for i, (h, w) in enumerate(zip(headers, widths))))
    for row in rows:
        print('  ' + '  '.join(str(c).ljust(w) if i == 0 else str(c).rjust(w) for i, (c, w) in enumerate(zip(row, widths))))


def print_timing(timed):
    rows = []
    for key, label, scale, unit in (
        ('wall', 'wall clock (client)', 1000, 'ms'),
        ('wsgi_time', 'wsgi_time (server)', 0.001, 'ms'),
        ('db_time', 'db_time', 0.001, 'ms'),
        ('db_count', 'db_count (SQL queries)', 1, ''),
    ):
        values = [t[key] for t in timed if key in t]
        if not values:
            continue
        median = statistics.median(values)
        spread = f'{min(values) * scale:.0f}-{max(values) * scale:.0f}'
        rows.append((label, f'{median * scale:.0f}{unit}', spread))
    print_table(f'Unprofiled timing, median of {len(timed)} runs', ('metric', 'median', 'min-max'), rows)


def print_key_functions(stats):
    rows = []
    for label, suffix, funcname in KEY_FUNCTIONS:
        values = find_function(stats, suffix, funcname)
        if values:
            _, ncalls, tottime, cumtime, _ = values
            rows.append((label, ncalls, f'{tottime * 1000:.1f}', f'{cumtime * 1000:.1f}'))
    embeds = find_function(stats, 'snovault/embed.py', 'embed')
    renders = find_function(stats, 'snovault/embed.py', '_embed')
    print_table('Key function call counts (profiled run)', ('function', 'calls', 'own ms', 'cumulative ms'), rows)
    if embeds and renders:
        hits = embeds[1] - renders[1]
        print(f'  embed cache: {hits} of {embeds[1]} request.embed calls were not rendered '
              f'({hits / embeds[1]:.0%}); frameless and as_user embeds bypass the cache')


def print_categories(stats):
    totals = collections.Counter()
    for (filename, _, funcname), (_, _, tottime, _, _) in stats.stats.items():
        totals[category_of(filename, funcname)] += tottime
    grand = sum(totals.values()) or 1.0
    rows = [(name, f'{seconds * 1000:.0f}', f'{seconds / grand:.0%}') for name, seconds in totals.most_common()]
    print_table('Time spent in each layer\'s own code (profiled, exclusive)', ('layer', 'ms', 'share'), rows)


def print_top_functions(stats, sortby, limit):
    index = {'tottime': 2, 'cumtime': 3}[sortby]
    ranked = sorted(stats.stats.items(), key=lambda item: item[1][index], reverse=True)[:limit]
    rows = [(short_name(key)[:78], v[1], f'{v[2] * 1000:.1f}', f'{v[3] * 1000:.1f}') for key, v in ranked]
    print_table(f'Top {limit} functions by {sortby}', ('function', 'calls', 'own ms', 'cumulative ms'), rows)


def print_embed_trace(tracer, limit):
    if not tracer.records:
        print('\nNo subrequest renders recorded.')
        return
    ranked = sorted(tracer.records.items(), key=lambda item: item[1]['exclusive'], reverse=True)[:limit]
    rows = [
        (f'{collection} {frame}'[:78], r['count'], r['uncached'], f'{r["exclusive"] * 1000:.1f}', f'{r["inclusive"] * 1000:.1f}')
        for (collection, frame), r in ranked
    ]
    print_table(
        f'Subrequest renders by (collection, frame), top {limit} by own time',
        ('collection frame', 'renders', 'uncached', 'own ms', 'incl ms'),
        rows,
    )
    distinct_paths = len(tracer.path_counts)
    repeats = sum(count - 1 for count in tracer.path_counts.values())
    multi_frame = [item for item, frames in tracer.item_frames.items() if len(frames) > 1]
    print(f'  {tracer.total_renders} renders of {distinct_paths} distinct path+frame '
          f'({repeats} repeats the embed cache did not absorb)')
    print(f'  {len(multi_frame)} of {len(tracer.item_frames)} items were rendered in more than one frame')
    worst = sorted(tracer.item_frames.items(), key=lambda item: len(item[1]), reverse=True)[:5]
    for item, frames in worst:
        if len(frames) > 1:
            print(f'    {item}: {len(frames)} frames')


def print_sql_trace(tracer, limit):
    if not tracer.counts:
        print('\nNo SQL statements recorded.')
        return
    by_statement = collections.Counter()
    for (statement, _), count in tracer.counts.items():
        by_statement[statement] += count
    rows = [(f'{statement}'[:100], count) for statement, count in by_statement.most_common(limit)]
    print_table(f'SQL statements, top {limit} of {len(by_statement)} kinds ({tracer.total} total)', ('statement', 'count'), rows)
    rows = []
    for (statement, site), count in tracer.counts.most_common(limit):
        frames = site.split(' <- ')
        rows.append((' <- '.join(frames[:3])[:80], ' <- '.join(frames[3:])[:80], statement[:60], count))
    print_table(
        f'SQL statements by calling code, top {limit}',
        ('called from (innermost first)', 'which was called from', 'statement', 'count'),
        rows,
    )


def print_key_lookups(tracer, limit):
    total = sum(tracer.key_lookups.values())
    if not total:
        return
    repeats = total - len(tracer.key_lookups)
    by_name = collections.Counter()
    for (name, _), count in tracer.key_lookups.items():
        by_name[name] += count
    print(f'\nUnique-key lookups: {total} queries for {len(tracer.key_lookups)} distinct (key, value) pairs; '
          f'{repeats} repeat a pair already queried')
    print_table('By key name', ('key name', 'queries'), by_name.most_common(limit))
    ranked = tracer.key_lookups.most_common(limit)
    print_table(f'Most frequent lookups, top {limit}', ('key name', 'value', 'queries'),
                [(name[:40], value[:60], count) for (name, value), count in ranked])


def print_callers_of(stats, funcnames, limit):
    rows = []
    for (filename, lineno, funcname), values in stats.stats.items():
        if funcname in funcnames:
            for caller, counts in sorted(values[4].items(), key=lambda item: item[1][1], reverse=True)[:limit]:
                rows.append((funcname, short_name(caller)[:70], counts[1] if isinstance(counts, tuple) else counts))
    if rows:
        print_table('Who calls these functions (calls)', ('function', 'called by', 'calls'), rows)


def print_audit_checkers(stats, limit):
    ranked = sorted(
        ((key, values) for key, values in stats.stats.items() if package_relative(key[0]).startswith('igvfd/audit/')),
        key=lambda item: item[1][3], reverse=True,
    )[:limit]
    rows = [
        (short_name(key)[:78], values[1], f'{values[2] * 1000:.1f}', f'{values[3] * 1000:.1f}')
        for key, values in ranked
    ]
    if rows:
        print_table(f'igvfd audit functions by cumulative time, top {limit}', ('function', 'calls', 'own ms', 'cumulative ms'), rows)


def run_mode(testapp, path, mode, args):
    url = add_query(path, datastore=args.datastore or None, batch_embed=mode)

    def fetch():
        response = testapp.get(url, expect_errors=True)
        if response.status_int != 200:
            hint = ' (index-data-external needs --username INDEXER)' if response.status_int == 403 else ''
            sys.exit(f'GET {url} returned {response.status_int}{hint}')
        return response

    for _ in range(args.warm_ups):
        fetch()
    timed = []
    for _ in range(args.runs):
        start = time.perf_counter()
        response = fetch()
        wall = time.perf_counter() - start
        timed.append({'wall': wall, **parse_x_stats(response.headers.get('X-Stats', ''))})

    tracer = EmbedTracer()
    sql_tracer = SqlTracer()
    profile = cProfile.Profile()
    tracer.install()
    sql_tracer.install()
    try:
        profile.enable()
        response = fetch()
        profile.disable()
    finally:
        sql_tracer.remove()
        tracer.remove()
    try:
        body = response.json
    except ValueError:
        body = response.text
    stats = pstats.Stats(profile)

    print(f'\n{"=" * 100}\nbatch_embed={mode}   GET {url}\n{"=" * 100}')
    if timed:
        print_timing(timed)
    print_categories(stats)
    print_key_functions(stats)
    print_embed_trace(tracer, args.top)
    print_sql_trace(sql_tracer, args.top)
    print_key_lookups(sql_tracer, args.top)
    print_callers_of(stats, ('effective_principals', 'has_permission'), 5)
    print_audit_checkers(stats, args.top)
    print_top_functions(stats, args.sortby, args.top)
    if args.out:
        os.makedirs(args.out, exist_ok=True)
        filename = os.path.join(args.out, f'batch_embed_{mode}.prof')
        stats.dump_stats(filename)
        print(f'\nsaved {filename}')
    return timed, stats, tracer, body


IGNORED_KEYS = ('xmin',)


def normalize_json(value):
    """Sort every list so documents compare equal regardless of unspecified list order."""
    if isinstance(value, dict):
        return {key: normalize_json(member) for key, member in value.items()}
    if isinstance(value, list):
        return sorted((normalize_json(member) for member in value), key=lambda m: json.dumps(m, sort_keys=True, default=str))
    return value


def find_differences(left, right, path='$', limit=10):
    """Up to `limit` (path, left, right) differences between two JSON-like values."""
    differences = []

    def walk(a, b, where):
        if len(differences) >= limit:
            return
        if type(a) is not type(b):
            differences.append((where, repr(a)[:60], repr(b)[:60]))
        elif isinstance(a, dict):
            for key in sorted(set(a) | set(b)):
                if key not in a or key not in b:
                    differences.append((f'{where}.{key}', 'missing' if key not in a else '...', 'missing' if key not in b else '...'))
                else:
                    walk(a[key], b[key], f'{where}.{key}')
        elif isinstance(a, list):
            if len(a) != len(b):
                differences.append((where, f'{len(a)} items', f'{len(b)} items'))
            else:
                for index, (x, y) in enumerate(zip(a, b)):
                    walk(x, y, f'{where}[{index}]')
        elif a != b:
            differences.append((where, repr(a)[:60], repr(b)[:60]))

    walk(left, right, path)
    return differences


def drop_ignored(body):
    if isinstance(body, dict):
        return {key: value for key, value in body.items() if key not in IGNORED_KEYS}
    return body


def print_body_comparison(results):
    modes = list(results)
    left, right = (drop_ignored(results[mode][3]) for mode in modes[:2])
    if left == right:
        print(f'\nResponse bodies: identical, including list order (ignoring {", ".join(IGNORED_KEYS)})')
        return
    differences = find_differences(normalize_json(left), normalize_json(right))
    if not differences:
        print('\nResponse bodies: same content; only the order of some list members differs')
        return
    print(f'\nResponse bodies DIFFER between batch_embed={modes[0]} and batch_embed={modes[1]} (first {len(differences)}):')
    for where, a, b in differences:
        print(f'  {where}: {a}  !=  {b}')


def print_comparison(results):
    rows = []
    for key, label, scale in (('wall', 'wall ms', 1000), ('wsgi_time', 'wsgi ms', 0.001),
                              ('db_time', 'db ms', 0.001), ('db_count', 'db queries', 1)):
        cells = []
        for mode in results:
            values = [t[key] for t in results[mode][0] if key in t]
            cells.append(f'{statistics.median(values) * scale:.0f}' if values else '-')
        rows.append((label, *cells))
    rows.append(('subrequest renders', *[results[mode][2].total_renders for mode in results]))
    print_table('Comparison (medians of unprofiled runs)', ('metric', *[f'batch_embed={m}' for m in results]), rows)


def get_parser():
    parser = argparse.ArgumentParser(
        description='Profile igvfd rendering of a URL. GET only.',
        epilog=__doc__,
        formatter_class=argparse.RawDescriptionHelpFormatter,
    )
    parser.add_argument('config_uri', help='path to ini file, e.g. config/pyramid/ini/development.ini')
    parser.add_argument('path', help='URL path to render, e.g. /analysis-sets/IGVFDS5575ANST/@@index-data-external')
    parser.add_argument('--app-name', default='app', help='Pyramid app name in the config file')
    parser.add_argument('--username', '-u', default='INDEXER', help='remote user (INDEXER can view index-data-external)')
    parser.add_argument('--datastore', default='database',
                        help='datastore query param; use database so items are computed, not served from ES (empty to omit)')
    parser.add_argument('--batch-embed', choices=['true', 'false', 'both'], default='both')
    parser.add_argument('--warm-ups', type=int, default=1, help='unmeasured requests per mode')
    parser.add_argument('--runs', type=int, default=3, help='unprofiled timing requests per mode')
    parser.add_argument('--top', type=int, default=25, help='rows per table')
    parser.add_argument('--sortby', choices=['tottime', 'cumtime'], default='tottime')
    parser.add_argument('--out', help='directory to save .prof files')
    return parser


def main():
    args = get_parser().parse_args()
    from pyramid.paster import get_app
    from webtest import TestApp
    app = get_app(args.config_uri, args.app_name)
    testapp = TestApp(app, {'HTTP_ACCEPT': 'application/json', 'REMOTE_USER': args.username})
    modes = ['false', 'true'] if args.batch_embed == 'both' else [args.batch_embed]
    results = {mode: run_mode(testapp, args.path, mode, args) for mode in modes}
    if len(results) > 1:
        print(f'\n{"=" * 100}')
        print_comparison(results)
        print_body_comparison(results)


if __name__ == '__main__':
    main()
