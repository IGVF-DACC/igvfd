import json
import logging

import pytest

from igvfd.audit import timing
from igvfd.audit.timing import run_audits_with_timing


def audit_one(value, system):
    yield 'failure-a'


def audit_two(value, system):
    yield 'failure-b1'
    yield 'failure-b2'


def audit_none(value, system):
    return
    yield  # pragma: no cover - makes this a generator function


FUNCTION_DISPATCHER = {
    'audit_one': audit_one,
    'audit_two': audit_two,
    'audit_none': audit_none,
}


EXPECTED_FAILURES = ['failure-a', 'failure-b1', 'failure-b2']


class _RecordingHandler(logging.Handler):
    def __init__(self):
        super().__init__()
        self.records = []

    def emit(self, record):
        self.records.append(record)


@pytest.fixture
def timing_log_handler():
    handler = _RecordingHandler()
    previous_level = timing.logger.level
    timing.logger.addHandler(handler)
    timing.logger.setLevel(logging.INFO)
    try:
        yield handler
    finally:
        timing.logger.removeHandler(handler)
        timing.logger.setLevel(previous_level)


def test_run_audits_with_timing_disabled_yields_failures_and_no_logs(monkeypatch, timing_log_handler):
    monkeypatch.setattr(timing, 'AUDIT_TIMING_ENABLED', False)
    value = {'@type': ['MeasurementSet']}
    failures = list(run_audits_with_timing(FUNCTION_DISPATCHER, value, {}, frame='object'))
    assert failures == EXPECTED_FAILURES
    assert timing_log_handler.records == []


def test_run_audits_with_timing_enabled_yields_failures_and_logs(monkeypatch, timing_log_handler):
    monkeypatch.setattr(timing, 'AUDIT_TIMING_ENABLED', True)
    value = {'@type': ['MeasurementSet'], 'uuid': 'abcd-1234'}
    failures = list(run_audits_with_timing(FUNCTION_DISPATCHER, value, {}, frame='object'))
    assert failures == EXPECTED_FAILURES
    assert len(timing_log_handler.records) == len(FUNCTION_DISPATCHER)
    payloads = [json.loads(record.getMessage()) for record in timing_log_handler.records]
    by_function = {payload['audit_function']: payload for payload in payloads}
    assert set(by_function) == set(FUNCTION_DISPATCHER)
    assert by_function['audit_two']['failure_count'] == 2
    assert by_function['audit_one']['failure_count'] == 1
    assert by_function['audit_none']['failure_count'] == 0
    for payload in payloads:
        assert payload['log_type'] == 'audit_timing'
        assert payload['item_type'] == 'MeasurementSet'
        assert payload['uuid'] == 'abcd-1234'
        assert payload['frame'] == 'object'
        assert isinstance(payload['elapsed_seconds'], float)


def test_run_audits_with_timing_enabled_defaults_item_type(monkeypatch, timing_log_handler):
    monkeypatch.setattr(timing, 'AUDIT_TIMING_ENABLED', True)
    failures = list(run_audits_with_timing(FUNCTION_DISPATCHER, {}, {}, frame='object'))
    assert failures == EXPECTED_FAILURES
    payloads = [json.loads(record.getMessage()) for record in timing_log_handler.records]
    assert all(payload['item_type'] == 'unknown' for payload in payloads)
    assert all(payload['uuid'] is None for payload in payloads)
