#!/bin/bash

#If there is a cli maker, why not make a script maker as well?

#name of the script
name=$1
#as this script only generates .sh files, the extension has to be added to the $name variable
file="$name.sh"

#prints usage
print_usage() {
	
	cat << EOF
	
	Usage: scriptmaker <NameOfFile>
	Output:
		No output. Creates a new shellscript file, with given name.
		Does not overwrite existing files.

EOF

}

#check if a script with the given name already exists in the current directory
if [ -f $file ]
then
	echo "File already exists"
	print_usage
	exit 1
else
	cat << EOF >>"$name.sh"
#!/bin/bash

#prints usage
print_usage() {
	#add usage message here
}

#main function
main() {
	#add main code here
}

#main function execution
main
EOF
fi

