#!/usr/bin/bash

# fetch latest change from github
git fetch -f
git reset --hard origin/HEAD

# save transaction list
mkdir temp/
docker-compose exec web python manage.py dumpdata accounts --indent 4 > temp/0_user.json
docker-compose exec web python manage.py dumpdata acc_books --indent 4 > temp/1_acc_book.json
docker-compose exec web python manage.py dumpdata acc_codes --indent 4 > temp/2_acc_codes.json
docker-compose exec web python manage.py dumpdata transactions --indent 4 > temp/3_transactions.json

# restart docker container and db volume
docker-compose down
docker volume rm fastreckon_postgres_data
docker-compose up -d --build
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py populate_account

echo "Start Load testdata"

docker-compose exec web python manage.py loaddata temp/0_user.json
docker-compose exec web python manage.py loaddata temp/1_mybook.json
docker-compose exec web python manage.py loaddata temp/2_myaccount.json
docker-compose exec web python manage.py loaddata temp/3_transactions.json
rmdir temp/

echo "Finish Load testdata"