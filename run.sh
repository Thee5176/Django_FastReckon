#!/usr/bin/bash

# build and migrate db
docker-compose up -d --build
docker-compose exec web python manage.py migrate

# # (Optional) populate data
# echo "Start Load testdata"

# docker-compose exec web python manage.py loaddata mytestdata/0_user.json
# docker-compose exec web python manage.py loaddata mytestdata/1_myaccount.json
# docker-compose exec web python manage.py loaddata mytestdata/2_mybook.json
# docker-compose exec web python manage.py loaddata mytestdata/3_myrecord.json

# echo "Finish Load testdata"