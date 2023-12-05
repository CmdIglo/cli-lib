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
    echo "      -o                 Specify input file name and print route map and route to stdout"
    echo ""
    echo ""
    echo "  Notice:"
    echo " ---------"
    echo "      You have to have python installed on your computer for the script to run properly"
    exit 1
}

function move_file() {
    local file1=$1
    local file2=$2

    cutfile1=$(echo "$file1" | cut -d'/' -f2)       #trim the file path at the "/"

    flpname=$(echo "$cutfile1" | cut -d'.' -f1)    #get the route name 
    flpext=$(echo "$cutfile1" | cut -d'.' -f2)     #get the route extension to determine if its pmdg or aerosoft
    if [[ "$flpext" == "flp" ]]; then               #if input file was .flp file
        firstarpt="${flpname:0:4}"                  #get the first airport
        sndarpt="${flpname:4}"                      #get the second airport
        filename="$firstarpt-$sndarpt.rte"          #the name of the file being created if it was converted from flp to rte
        if [ ! -d "$file2" ]; then                  #if directory doesnt exist, create it
            # If it doesn't exist, create it
            mkdir -p "$file2"
            #check if the dir was created succesfully
            if [ $? -eq 0 ]; then
                echo "Directory created: $file2"
                mv "$filename" "$file2"
            else
                echo "Failed to create directory: $file2"
                rm -rf "$filename"
                exit 1
            fi            
        else
            mv "$filename" "$file2"                 #else just move the file to the directory
        fi
        exit 0
    fi
    
    #everything that happens above, but for a flp plan that was created from a rte
    firstarpt=$(echo "$cutfile1" | cut -d'-' -f1)
    sndarpt=$(echo "$cutfile1" | cut -d'-' -f2 | cut -d'.' -f1)
    filename="$firstarpt$sndarpt.flp"
    if [ ! -d "$file2" ]; then
            # If it doesn't exist, create it
            mkdir -p "$file2"
            #check if the dir was created succesfully
            if [ $? -eq 0 ]; then
                echo "Directory created: $file2"
                mv "$filename" "$file2"
            else
                echo "Failed to create directory: $file2"
                rm -rf "$filename"
                exit 1
            fi 
        else
            mv "$filename" "$file2"
        fi
    exit 0
}

function installDepsLinux() {
    pip3 install numpy
    pip3 install matplotlib
    pip3 install Pillow
    sudo apt update
    sudo apt install libgeos-dev libproj-dev
    pip3 install basemap --user
}

function installDepsWin() {
    pip install numpy
    pip install matplotlib
    pip install Pillow
    for FILE in lib/basemap*; do
        if [[ -f $FILE ]]; then
            pip install $FILE
        fi
    done
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
                    installDepsLinux                    
                    python3 main.py -f "$file1" "$file2"
                    move_file "$file1" "$file2"
                    ;; 
                msys*) 
                    installDepsWin                    
                    python main.py -f "$file1" "$file2"
                    move_file "$file1" "$file2"
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
                    installDepsLinux
                    python3 main.py -o "$inputFile"
                    ;; 
                msys*) 
                    installDepsWin
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
