#!/bin/bash
echo "Starting deduplicator"
sleep 60
./dedup -numWorkers=${NUM_WORKERS} -queueURL=${QUEUE_URL} -runForever -secondsToSleepBetweenRuns=600
