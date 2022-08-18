#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
batchupgrade-with-notification config/pyramid/ini/production.ini --app-name app --processes 1 --batchsize 1000
