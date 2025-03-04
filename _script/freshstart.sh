#!/usr/bin/bash

./_script/backup.sh

# restart docker container and db volume
docker-compose down
docker volume rm fastreckon_postgres_data

./_script/rollback.sh

docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate_account

# load testdata then temp data

./_script/loaddata.sh