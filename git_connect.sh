#!/bin/bash

#initializing variables and functions

#Repo User Name
name=$1
#Repo Name
repo=$2
#Personal access token
token=$3

#function that performs a initial git commit
make_commit() {

	#write to readme file
	echo "# $repo" 1> README.md
	git init
	git add README.md
	git commit -m "Automated first commit"
	git branch -M main
	git remote add origin https://$token@github.com/$name/$repo
	git push -u origin main

}

echo "Initializing git repository"

#Script has to be executed in the directory, where the git projects are stored
#Check if folder for repo already exists
if [ -d $repo ] 
then
	cd $repo
else
	mkdir $repo
	cd $repo
fi

#Initial commit 
make_commit


