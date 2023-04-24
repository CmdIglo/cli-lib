#!/bin/bash

#initializing variables
#Repo User Name
name=$1
#Repo Name
repo=$2
#Personal access token
token=$3

echo "Initializing git repository"

#Script has to be executed in the directory, where the git projects are stored
mkdir $repo
cd $repo

#Initial commit 
echo "# $repo" 1> README.md
git init
git add README.md
git commit -m "Automated first commit"
git branch -M main
git remote add origin https://$token@github.com/$name/$repo
git push -u origin main

