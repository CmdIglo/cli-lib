# Flightplan converter

## Functionality

 Converter for .flp (aerosoft) and .rte (pmdg) Flightplan files. <br/> 
 Converts from .flp :left_right_arrow: .rte or makes a route map of given flightplan

 <code>Usage: conv.sh [-h] [-f inputFile outputFolder] [-o inputFile [-s|--save]]</code>

     -h, --help         Display this help message
     -f                 Specify input file name and print Route to provided folder
     -o                 Specify input file name and print Route to stdout
     -s, --save         Specify if the route map should be saved as .png (Yes if set else no)

 Notice:
---------
     You have to have python installed on your computer for the script to run properly. 
     Currently only works on Windows and Linux OS. For other OS clone this Repo and add 
     Python call for your machine in conv.sh.

## Get local copy

 Just clone this repo to a local folder on your machine:

 <code>git clone https://github.com/CmdIglo/cli-lib/tree/main/flpconv [storage location]</code>

## Basemap installation

 The Basemap pip library along with the other pip packages is being installed by the shell 
 script upon first execution.



:copyright: Maxwell Leu 2023
