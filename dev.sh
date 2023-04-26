#!/bin/bash

#prints usage of script
print_usage() {
	
	cat << EOF

	Usage: dev [-l] [-h|--help] <Project name>
	Output:
		No output. Changes directory from current to project directory

EOF
}

#is being executed, when the script runs into errors
nostd_exit() {
	print_usage
	exit 1
}

main() {

	local mode=
	local dir=
	local position=0
	
	while [[ "${#}" -gt 0 ]]; do
		case "${1}" in
			-h|--help)
				print_usage
				exit 0
				;;
			-l)
				echo "Set link for projects directory"
				exit 0
				;;
			*)
				case "${position}" in
					0)
						mode=${1}
						position=1
						shift
						;;
					1)
						dir=${1}
						position=2
						shift
						;;
					2)
						nostd_exit
						;;
				esac
				;;
		esac
	done

	echo $dir$mode

	#check if the project exists locally
	if [ -d $dir$mode ] 
	then
		cd $dir$mode
		echo "Project exists"
	else
		echo "Project does not exist locally"
		nostd_exit
	fi

	return 0
}

main "${@:-}"
