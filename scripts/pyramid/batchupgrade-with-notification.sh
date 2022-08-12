#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
export DEFAULT_MESSAGE_BUS=some.message.bus.com
batchupgrade-with-notification config/pyramid/ini/development.ini --app-name app --processes 1 --batchsize 1000
