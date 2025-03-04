#!/usr/bin/bash

cd FastReckon
pwd
ls -a

# Backup
echo "Running backup..."
./_script/backup.sh

# Fetch latest code
echo "Fetching latest code..."
./_script/fetch.sh