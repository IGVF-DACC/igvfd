#!/bin/bash
cd /igvfd
create-mapping config/pyramid/ini/development.ini --app-name app --dry-run > /asset-output/mapping.json
