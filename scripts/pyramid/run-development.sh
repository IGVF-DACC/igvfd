#!/bin/bash
export SESSION_SECRET=$(cat /dev/urandom | head -c 256 | base64)
gunicorn --config ./config/gunicorn/development.conf.py --paste ./config/pyramid/ini/development.ini --access-logfile '-' --access-logformat '%(h)s %(l)s %(u)s %(t)s "%(r)s" %(s)s %(b)s "%(f)s" "%(a)s" %({X-Stats}o)s'
