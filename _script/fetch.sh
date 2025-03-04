# backup record
./_script/backup.sh

# always keep backup file
git stash

git fetch -f
git checkout -b load
git checkout load
git reset --hard origin/main

# update excecution for new bash script
chmod +x `ls _script/*.sh`