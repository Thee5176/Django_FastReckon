# update excecution for new bash script
chmod +x `ls _script/*.sh`

git fetch -f
git reset --hard origin/HEAD
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py check