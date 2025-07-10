#!/usr/bin/bash

# fetch latest change from github
./_script/fetch.sh

# save transaction list
echo "Start backup data..."

mkdir temp/
docker-compose exec web python manage.py dumpdata accounts --indent 4 > temp/0_user.json
docker-compose exec web python manage.py dumpdata acc_books --indent 4 > temp/1_acc_book.json
docker-compose exec web python manage.py dumpdata acc_codes --indent 4 > temp/2_acc_codes.json
docker-compose exec web python manage.py dumpdata transactions --indent 4 > temp/3_transactions.json

echo "Finish backup data"

# restart docker container and db volume
docker-compose down
docker volume rm fastreckon_postgres_data
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate_account

# load testdata then temp data

./_script/loaddata.sh

echo "Start Load data"

docker-compose exec web python manage.py loaddata temp/0_user.json
docker-compose exec web python manage.py loaddata temp/1_acc_book.json
docker-compose exec web python manage.py loaddata temp/2_acc_codes.json
docker-compose exec web python manage.py loaddata temp/3_transactions.json
rm -rf temp/

echo "Finish Load data"