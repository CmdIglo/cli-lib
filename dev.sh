#!/bin/bash

#which project 
mode=$1
#projects dir
directory=$2
#-l flag for project listing; lists git projects available on the machine
list_flag=''

#prints usage of script
print_usage() {
	echo "Usage: dev [-l] <Projectname>" 1>&2
}

#is being executed, when the script runs into errors
nostd_exit() {
	print_usage
	exit 1
}

#check if a flag is set
while getopts "l" option; do
	case "${option}" in
		l)
			ls $directory | echo
			;;
		*)
			nostd_exit
			;;
	esac
done

#check if the project exists locally
if [ -d $directory$mode] 
then
	cd $directory$mode
else
	echo "Project does not exist locally"
	nostd_exit
fi
