#!/bin/bash

#which project 
mode=$1
#-l flag for project listing; lists git projects available on the machine
list_flag=''

#prints usage of script
print_usage() {
	echo "Usage: dev [-l] <Projectname>" 1>&2
}

while getopts "l:"
