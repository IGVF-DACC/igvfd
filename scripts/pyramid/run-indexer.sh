#!/bin/bash
sleep 15
export SESSION_SECRET=$(cat /dev/urandom | head -c 256 | base64)
gunicorn --config ./config/gunicorn/indexer.conf.py --paste ./config/pyramid/ini/indexer.ini#indexer
