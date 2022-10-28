#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
echo "DELETE MAPPINGS"
curl -XDELETE ${OPENSEARCH_URL}/*
create-mapping config/pyramid/ini/production.ini --app-name app
python src/igvfd/commands/reindex.py config/pyramid/ini/production.ini --app-name app
