#!/bin/bash
export SESSION_SECRET=$(cat /dev/urandom | head -c 256 | base64)
gunicorn --config ./config/gunicorn/development.conf.py --paste ./config/pyramid/ini/development.ini
