
import json
import os
import time
from collections import Counter
from urllib.parse import parse_qs

import pytest
from sqlalchemy import event
from sqlalchemy.engine import Engine

pytestmark = pytest.mark.skipif(
    not os.environ.get('PROFILE'), reason='local profiling only; set PROFILE=1'
)

LABEL = os.environ.get('LABEL', 'run')
OUT = '/igvfd/.profile'

CASES = [
    ('basic_analysis_set', '/analysis-sets/IGVFDS5575ANST/'),
]
FRAMES = [
    'object',
    'embedded',
    'audit',
    'object_with_select_calculated_properties&field=files',
]


def measure(testapp, url):
    link_statements = Counter()
    total = []

    def log(conn, cursor, statement, parameters, *args):
        total.append(statement)
        if 'FROM links' in statement:
            link_statements[(statement, repr(parameters))] += 1

    event.listen(Engine, 'before_cursor_execute', log)
    start = time.time()
    try:
        res = testapp.get(url)
    finally:
        event.remove(Engine, 'before_cursor_execute', log)
    stats = {k: v[0] for k, v in parse_qs(res.headers['X-Stats']).items()}
    links = sum(link_statements.values())
    return {
        'wall': round(time.time() - start, 2),
        'statements': len(total),
        'x_db_count': int(stats.get('db_count', 0)),
        'db_time': round(int(stats.get('db_time', 0)) / 1e6, 3),
        'link_statements': links,
        'link_repeats': links - len(link_statements),
    }


@pytest.mark.parametrize('name,path', CASES)
@pytest.mark.parametrize('frame', FRAMES)
def test_profile_rendering(workbook, testapp, name, path, frame):
    url = f'{path}?frame={frame}&datastore=database'
    testapp.get(url)  # warm up Postgres, not the per-request caches
    row = measure(testapp, url)
    row.update(label=LABEL, case=name, frame=frame)
    os.makedirs(OUT, exist_ok=True)
    with open(f'{OUT}/{LABEL}.jsonl', 'a') as f:
        f.write(json.dumps(row) + '\n')
    print(row)
