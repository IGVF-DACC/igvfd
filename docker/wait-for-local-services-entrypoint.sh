#!/bin/bash
while ! curl -s http://localstack:4566/_localstack/init | grep -q '\"READY\": true'; do
    echo 'Waiting for Localstack to become ready...';
    sleep 5;
    done;
echo 'Localstack is ready.';
while ! curl -s http://opensearch:9200 | grep -q '\"cluster_name\"'; do
    echo 'Waiting for Opensearch to become ready...';
    sleep 5;
    done;
echo 'Opensearch is ready.';

exec "$@"
