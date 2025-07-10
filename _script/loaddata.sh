docker-compose exec web python manage.py migrate

echo "Start Load testdata"

docker-compose exec web python manage.py loaddata _testdata/0_user.json
docker-compose exec web python manage.py loaddata _testdata/1_book.json
docker-compose exec web python manage.py loaddata _testdata/2_account.json
docker-compose exec web python manage.py loaddata _testdata/3_record.json

echo "Finish Load testdata"