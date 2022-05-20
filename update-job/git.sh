#!/bin/sh
set -eux
cd ..
user=$1
repo=$2
token=$3
git add -A
git commit -m "Updating repo"
git push https://$token@github.com/$user/$repo.git
