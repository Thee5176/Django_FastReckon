# backup record
./_script/dumpdata.sh

git fetch -f
git reset --hard origin/main

# update excecution for new bash script
chmod +x `ls _script/*.sh`

git stash pop