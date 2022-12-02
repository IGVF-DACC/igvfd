#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
batchupgrade config/pyramid/ini/${INI_NAME} --app-name app --processes 1 --batchsize 1000
