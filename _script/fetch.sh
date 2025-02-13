# backup record
./_script/dumpdata.sh

git stash
git fetch -f
git reset --hard origin/main

# update excecution for new bash script
chmod +x `ls _script/*.sh`

echo "check migrations file..."
docker-compose exec web python manage.py migrate
docker-compose exec web python manage.py check

git stash pop