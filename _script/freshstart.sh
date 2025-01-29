#!/usr/bin/bash

# fetch latest change from github
git fetch -f

# restart docker container and db volume
docker-compose down
docker volume rm fastreckon_postgres_data
docker-compose up -d --build
docker-compose exec web python manage.py migrate

echo "Start Load testdata"

docker-compose exec web python manage.py loaddata mytestdata/0_user.json
docker-compose exec web python manage.py loaddata mytestdata/1_myaccount.json
docker-compose exec web python manage.py loaddata mytestdata/2_mybook.json
docker-compose exec web python manage.py loaddata mytestdata/3_myrecord.json

echo "Finish Load testdata"