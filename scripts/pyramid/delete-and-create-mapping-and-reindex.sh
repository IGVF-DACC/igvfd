#!/bin/bash
export SQLALCHEMY_URL=postgresql://postgres:${DB_PASSWORD}@${DB_HOST}/${DB_NAME}
export OPENSEARCH_URL=$OPENSEARCH_FOR_WRITING_URL
echo "MANAGE MAPPINGS"
python src/igvfd/commands/maybe_migrate_from_old_to_new_opensearch_indices.py --opensearch-url $OPENSEARCH_URL
manage-mappings-with-notification config/pyramid/ini/${INI_NAME} --app-name app --should-reindex always --relative-mapping-directory src/igvfd/mappings
