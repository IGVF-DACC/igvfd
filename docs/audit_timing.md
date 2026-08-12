# Audit timing instrumentation

This describes how to profile the per-function execution time of the audits in
`src/igvfd/audit/` and how to aggregate the results in CloudWatch Logs Insights.

## How it works

Every audit dispatcher runs its audit functions through
`run_audits_with_timing` in [src/igvfd/audit/timing.py](../src/igvfd/audit/timing.py).
When timing is enabled it wraps the full consumption of each audit generator and
emits one JSON log line per function, via the `igvfd.audit.timing` logger, e.g.:

```
INFO [igvfd.audit.timing][MainThread] {"log_type": "audit_timing", "audit_function": "audit_upload_status", "item_type": "SequenceFile", "uuid": "1a2b3c4d-0000-1111-2222-333344445555", "frame": "object", "elapsed_seconds": 0.000123, "failure_count": 0}
```

The `uuid` identifies the specific item that was audited, so slow individual
objects can be traced back to the source record.

Audits run in the pyramid backend container (the indexing service fetches
indexable documents, which include computed audits, from the backend), so the
timing logs land in the backend `pyramid` log group.

Timing is gated by the `AUDIT_TIMING_ENABLED` environment variable and is
**off by default in every environment**. The flag is read once at import time,
so a task must start fresh (a rolling deploy) to pick up a change.

## Enabling for a profiling run

1. Set `audit_timing_enabled` to `True` for the target environment's `backend`
   block in [cdk/infrastructure/config.py](../cdk/infrastructure/config.py):

   ```python
   'backend': {
       ...
       'ini_name': 'production.ini',
       'audit_timing_enabled': True,
       ...
   },
   ```

   This sets `AUDIT_TIMING_ENABLED=true` on the pyramid `ApplicationContainer`.
   The `igvfd.audit.timing` logger is already configured at `INFO` in the deploy
   ini files (`production.ini`, `staging.ini`, `sandbox.ini`, `demo.ini`).

2. Deploy the environment.

3. Trigger a full reindex so every object is audited (see
   [src/igvfd/commands/reindex.py](../src/igvfd/commands/reindex.py), which posts
   to `/_reindex`).

4. Collect and aggregate the logs (below).

5. When finished, set `audit_timing_enabled` back to `False` (or remove the key)
   and redeploy to stop the log volume.

## Running locally with docker compose

The `pyramid` service in `docker-compose.yml` and `docker-compose.test-indexer.yml`
reads `AUDIT_TIMING_ENABLED` (default `false`). Enable it by exporting the
variable before bringing the stack up:

```bash
# Full local stack: loads dev data and indexes it, running audits with timing on.
AUDIT_TIMING_ENABLED=true docker compose up --build

# Indexer integration tests with timing on.
AUDIT_TIMING_ENABLED=true docker compose -f docker-compose.test-indexer.yml up --exit-code-from indexer-tests
```

The `development.ini` used by the local `pyramid` service already configures the
`igvfd.audit.timing` logger at `INFO`, so the JSON lines appear in that service's
logs, e.g.:

```bash
AUDIT_TIMING_ENABLED=true docker compose up -d
docker compose logs -f pyramid | grep audit_timing
```

## Aggregating in CloudWatch Logs Insights

Run this against the backend `pyramid` log group. The JSON payload is prefixed
by the log formatter, so the fields are extracted with `parse`:

```
fields @timestamp, @message
| filter @message like /audit_timing/
| parse @message /"audit_function": "(?<audit_function>[^"]+)"/
| parse @message /"item_type": "(?<item_type>[^"]+)"/
| parse @message /"elapsed_seconds": (?<elapsed_seconds>[0-9.]+)/
| stats count(*) as n,
        avg(elapsed_seconds) as avg_s,
        pct(elapsed_seconds, 50) as p50,
        pct(elapsed_seconds, 90) as p90,
        max(elapsed_seconds) as max_s,
        sum(elapsed_seconds) as total_s
    by audit_function, item_type
| sort total_s desc
```

- `total_s` surfaces aggregate cost (slow x frequent), the best signal for what
  to optimize first.
- `p90` / `max_s` surface per-call outliers.
- Drop `item_type` from the `by` clause to aggregate a function across all types.

## Notes

- With timing disabled the code path is a single boolean check plus the original
  dispatch loop, so there is no meaningful overhead.
- One log line is emitted per (object x audit function). Over a full reindex this
  is a large but one-off volume; turn the flag back off once the run is done.
