git fetch -f
git reset --hard origin/HEAD
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py check