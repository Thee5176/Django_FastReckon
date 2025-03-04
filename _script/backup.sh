docker-compose exec web python manage.py migrate

docker-compose exec web python manage.py dumpdata accounts --indent 4 > _testdata/0_user.json
docker-compose exec web python manage.py dumpdata acc_books --indent 4 > _testdata/1_book.json
docker-compose exec web python manage.py dumpdata acc_codes --indent 4 > _testdata/2_account.json
docker-compose exec web python manage.py dumpdata transactions --indent 4 > _testdata/3_record.json