#!/bin/bash
sleep 10
manage-mappings config/pyramid/ini/development.ini --app-name app --should-reindex after-initial
