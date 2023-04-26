#!/bin/bash

#prints usage of script
print_usage() {
	
	cat << EOF

	Usage: dev [-l <LinkToProject>] [-h|--help] <ProjectName>
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

	#which project
	local mode=
	#directory; only temporary, for test reasons
	local dir=
	#in the stable build of this script, this variable is used to set the link of the projects directory
	local link=
	local position=0
	
	#iterate over the flags and positional arguments given
	while [[ "${#}" -gt 0 ]]; do
		case "${1}" in
			-h|--help)
				print_usage
				exit 0
				;;
			-l|--link)
				link="${2}"
				[[ -z "${link}" ]] && echo "No link proided" >&2 && print_usage >&2 && exit 1
				echo "Setting link for project directory"
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
