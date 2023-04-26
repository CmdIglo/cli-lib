#!/bin/bash

#@author: Maxwell Leu
#This script automates the connection process, between a local project
#directory and the corresponding git repo.
#This script has to be executed in the top level folder of the project directory.
#The Folder structure has to look like this:
#   "Projects"-dir
#	- Project 1 folder
#       - Project 2 folder
#	...
#Script has to be executed in the "Projects" directory

#initializing variables and functions; the "data" section

#print script usage
print_usage() {

	cat << EOF
	
	Usage: git_connect [-h|--help] <name> <repo name> <personal access token>
	Output:
		No output. Connects local repo file directory to git repo

EOF

}

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


#Executing the script, this is where all the magic happens; the "main", "text" section
main() {
	
	#Repo User Name
	local name=
	#Repo Name
	local repo=
	#Personal access token
	local token=
	#which position is being checked
	local position=0

	#check all flags and positional arguments
	while [[ "${#}" -gt 0 ]]; do
		case "${1}" in
			-h|--help)
				print_usage
				exit 0
				;;

			*)
			#if no flag is found, proceed to positional arguments
			case "${position}" in
				0)
					name=${1}
					position=1
					shift
					;;
				1)
					repo=${1}
					position=2
					shift
					;;
				2)
					token=${1}
					position=3
					shift
					;;
				3)
					echo "Unknown argument"
					print_usage
					exit 1
					;;
			esac
			;;
		esac
	done

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

	return 0
}

#main execution
main "${@:-}"
