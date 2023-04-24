#!/bin/bash

#initializing variables
#Repo Name
name=$1
#Repo URL
repo=$2
#Personal access token
token=$3

echo "Initializing git repository"
git init
git add README.md
git commit -m "Automated first commit"
git branch -M main
git remote add origin repo
git push -u origin main
