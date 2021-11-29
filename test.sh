#!/usr/bin/bash
export FLASK_ENV=development

echo 'Actual db will be renamed to old_blacklist_ms.db'
echo 'Remember to rename it if you want to use'
mv -f blacklist_ms.db old_blacklist_ms.db || echo 'blacklist_ms.db not exists... continue with tests'

pytest -s --cov mib

mv -f blacklist_ms.db blacklist_ms_test.db
( mv -f old_blacklist_ms.db blacklist_ms.db && rm -f blacklist_ms_test.db ) || ( echo 'old_blacklist_ms.db not exists... blacklist_ms.db from test will be held' && mv -f blacklist_ms_test.db blacklist_ms.db )

echo 'Test done!'