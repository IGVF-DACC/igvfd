#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
export OPENSEARCH_URL=$OPENSEARCH_FOR_WRITING_URL
echo "MANAGE MAPPINGS"
manage-mappings config/pyramid/ini/${INI_NAME} --app-name app
