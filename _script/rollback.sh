#!/usr/bin/bash

echo "Restoring backup..."

git reset --hard main

git stash pop