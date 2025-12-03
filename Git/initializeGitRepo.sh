#!/bin/sh

#  initializeGitRepo.sh
#  

mkdir $1
cd $1

echo "Initializing"
git init
echo "Adding README.md"
echo $3 >> README.md
git add *
echo "Committing"
git commit -m "first commit"
git remote add origin $2
echo "Pushing"
git push -u origin master
