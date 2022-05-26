#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
gunicorn --config ./config/gunicorn/gunicorn.conf.py --paste ./config/pyramid/ini/fargate.ini
