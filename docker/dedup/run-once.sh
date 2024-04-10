#!/bin/bash
echo "Running once"
echo ${NUM_WORKERS} ${QUEUE_URL}
./dedup -numWorkers=${NUM_WORKERS} -queueURL=${QUEUE_URL}
