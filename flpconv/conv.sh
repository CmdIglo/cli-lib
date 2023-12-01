#!/bin/bash

# Function to display help
function display_help() {
    echo " -----------------------------------------------------------------" 
    echo "  Converter for .flp (aerosoft) and .rte (pmdg) Flightplan files. "
    echo "  Converts from .flp <-> .rte"
    echo " -----------------------------------------------------------------"
    echo ""
    echo "  Usage: $0 [-h] [-f inputFile outputFolder] [-o inputFile]"
    echo ""
    echo "      -h, --help         Display this help message"
    echo "      -f                 Specify input file name and print Route to provided folder"
    echo "      -o                 Specify input file name and print Route to stdout"
    echo ""
    echo ""
    echo "  Notice:"
    echo " ---------"
    echo "      You have to have python installed on your computer for the script to run properly"
    exit 1
}

# Check for the number of arguments
if [ "$#" -eq 0 ]; then
    echo "Error: No options provided"
    display_help
fi

# Parse command-line options
while [[ $# -gt 0 ]]; do
    case $1 in
        -h|--help)
            display_help
            ;;
        -f)
            shift
            file1=$1
            shift
            file2=$1
            shift
            case "$OSTYPE" in
                linux*) 
                    python3 main.py -f "$file1" "$file2"
                    ;; 
                msys*) 
                    python main.py -f "$file1" "$file2"
                    ;;
                *) 
                    echo "Error: Unknown OS."
                    display_help
                    ;;
            esac
            exit 0
            ;;
        -o)
            shift
            inputFile=$1
            shift
            case "$OSTYPE" in
                linux*) 
                    python3 main.py -o "$inputFile"
                    ;; 
                msys*) 
                    python main.py -o "$inputFile"
                    ;;
                *) 
                    echo "Error: Unknown OS."
                    display_help
                    ;;
            esac
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            display_help
            ;;
    esac
done

# Check if the required options are provided
if [ -z "$file1" ] && [ -z "$inputFile" ]; then
    echo "Error: Please provide either -f or -o option."
    display_help
fi
