import json
import logging
import os
import time


logger = logging.getLogger('igvfd.audit.timing')


AUDIT_TIMING_ENABLED = os.environ.get('AUDIT_TIMING_ENABLED', '').lower() in ('1', 'true', 'yes')


def run_audits_with_timing(function_dispatcher, value, system, frame):
    """Run every audit function in a dispatcher, yielding failures unchanged.

    When AUDIT_TIMING_ENABLED is set, wraps the full consumption of each audit
    generator and emits one JSON log line per function for CloudWatch Logs
    Insights aggregation.
    """
    if not AUDIT_TIMING_ENABLED:
        for name in function_dispatcher:
            yield from function_dispatcher[name](value, system)
        return
    item_type = (value.get('@type') or ['unknown'])[0]
    uuid = value.get('uuid')
    for name, audit_function in function_dispatcher.items():
        start = time.perf_counter()
        failure_count = 0
        try:
            for failure in audit_function(value, system):
                failure_count += 1
                yield failure
        finally:
            logger.info(
                json.dumps(
                    {
                        'log_type': 'audit_timing',
                        'audit_function': name,
                        'item_type': item_type,
                        'uuid': uuid,
                        'frame': frame,
                        'elapsed_seconds': round(time.perf_counter() - start, 6),
                        'failure_count': failure_count,
                    }
                )
            )
