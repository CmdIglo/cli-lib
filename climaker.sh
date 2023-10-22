#!/bin/bash

#This script will make any shell script from this repo a CLI
#Note that the script has to be saved on the machine this script is running on

#Filename of the script
filename=$1

cp $filename "$filename"

echo $PATH 

ls
