#!/bin/bash
echo "Running once"
./dedup -numWorkers=${NUM_WORKERS} -queueURL=${QUEUE_URL}
