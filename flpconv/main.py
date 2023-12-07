
import os
import sys
import re
from argparse import ArgumentParser
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.basemap import Basemap
from itertools import chain
from PIL import Image

def plotRoute(rte):
    lats = []
    longs = []
    names = []
    for wpt_ in rte.getWaypoints():
        names.append(wpt_.getName())
    #check if rte or flp
    if "," in rte.getWaypoints()[0].getCoords():
        for wpt in rte.getWaypoints():
            lats.append(float(wpt.getCoords().split(",")[0]))
            longs.append(float(wpt.getCoords().split(",")[1]))
    else:
        for wpt in rte.getWaypoints():
            coords = wpt.getCoords().split(" ")
            lat = coords[2] if coords[1] == "N" else -1*float(coords[2])
            lon = coords[4] if coords[3] == "E" else -1*float(coords[4])
            lats.append(float(lat))
            longs.append(float(lon))

    scaled_lons = []
    for lon in longs:
        if lon < 0:
            scaled_lons.append(lon%180)
        else:
            scaled_lons.append(lon+180)

    scaled_lats = []
    for lat in lats:
        if lat < 0:
            scaled_lats.append(lat%90)
        else:
            scaled_lats.append(lat+90)

    lat_min = min(scaled_lats)-5
    lat_max = max(scaled_lats)+5
    lon_min = min(scaled_lons)-5
    lon_max = max(scaled_lons)+5

    lat_min = lat_min % 180 
    lat_max = lat_max % 180
    lon_min = lon_min % 360
    lon_max = lon_max % 360

    lat_min = (lat_min - 90) if lat_min >= 90 else (-1 * (90 - lat_min)) 
    lat_max = (lat_max - 90) if lat_max >= 90 else (-1 * (90 - lat_max))
    lon_min = (lon_min - 180) if lon_min >= 180 else (-1 * (180 - lon_min))
    lon_max = (lon_max - 180) if lon_max >= 180 else (-1 * (180 - lon_max))   

    plt.figure(figsize=(8, 8))
    
    llcornerlon = lon_min
    llcornerlat = lat_min
    urcornerlon = lon_max
    urcornerlat = lat_max

    m = Basemap(projection='cyl',  resolution='i',
            llcrnrlon=llcornerlon, llcrnrlat=llcornerlat,
            urcrnrlon=urcornerlon, urcrnrlat=urcornerlat,)    

    lons, latts = m(longs, lats)

    # draw a shaded-relief image
    # m.shadedrelief(scale=0.2)
    m.fillcontinents(color='0.8', lake_color=None, ax=None, zorder=None, alpha=None)
    m.drawcoastlines()   
    filename = rte.getStart()[0:-1] + rte.getEnd()[0:-1] + ".png" 
    m.plot(lons, latts, '-', markersize=5, linewidth=2) 
    plt.savefig(filename, bbox_inches='tight')
    img = Image.open(filename)
    width, height = img.size
    aspect_ratio = height/width
    new_width = 60
    new_height = aspect_ratio * new_width * 0.55
    img = img.resize((new_width, int(new_height)))
    img = img.convert('L')
    pixels = img.getdata()
    chars = ["-","/","_","@","$","%","*","|",":",".","\\", "l", "<", ">", "#", "§", "(", "´", "~"]
    new_pixels = [chars[pixel//14] for pixel in pixels]
    new_pixels = ''.join(new_pixels)
    new_pixels_count = len(new_pixels)
    ascii_image = [new_pixels[index:index + new_width] for index in range(0, new_pixels_count, new_width)]
    ascii_image = "\n".join(ascii_image)
    print(ascii_image)

#represents a .flp flight plan
class RouteFLP():
    def __init__(self, waypoints, start, end):
        self.waypoints = waypoints
        self.start = start
        self.end = end

    def getWaypoints(self):
        return self.waypoints

    def setWaypoints(self, wps):
        self.waypoints = wps

    def getStart(self):
        return self.start

    def setStart(self, start):
        self.start = start

    def getEnd(self):
        return self.end

    def setEnd(self, end):
        self.end = end

    def printRte(self, stream):
        if stream == "stdout":
            for wpt in self.waypoints:
                print("Waypoint:" + wpt.getName() + "At:" + wpt.getCoords())
        #prints to a file (the file is being moved into the given folder by the bash script)
        else:
            filename = self.start[0:-1] + self.end[0:-1] + ".flp"
            with open(filename, 'w') as file:
                file.write('''
[CoRte]
ArptDep=''' + self.start[0:-1] + '''
ArptArr=''' + self.end[0:-1] + '''
RwyDep=
RwyArr=
RwyArrFinal=
SID=
STAR=
APPR_Trans=''')  
                i = 1
                for wpt in self.waypoints:
                    qualifier = "\nDctWpt"+str(i) 
                    file.write(qualifier+"="+wpt.getName()[0:-1])
                    file.write(qualifier+"Coordinates="+wpt.getCoords())
                    i += 1       

#represents a .rte flight plan
class RouteRTE():
    def __init__(self, waypoints, start, end):
        self.waypoints = waypoints
        self.start = start
        self.end = end

    def getWaypoints(self):
        return self.waypoints

    def setWaypoints(self, wps):
        self.waypoints = wps

    def getStart(self):
        return self.start

    def setStart(self, start):
        self.start = start

    def getEnd(self):
        return self.end

    def setEnd(self, end):
        self.end = end

#TODO complete print rte function 
    def printRte(self, stream):
        if stream == "stdout":
            for wpt in self.waypoints:
                print("Waypoint:" + wpt.getName() + "At:" + wpt.getCoords())
        else:
            filename = self.start[0:-1] + "-" + self.end[0:-1] + ".rte"
            file = open(filename, "x")
            file.write("Generated by flpconv \u00a9 Maxwell Leu\n\n")
            file.write(str(len(self.waypoints)) + "\n\n")
            file.write(self.start[0:-1] + '''
1
DIRECT
1 COORDINATES HERE AND HEIGHT
-----
1
0

1
HEIGHT OF ARPT IN FT
-
-1000000
-1000000\n\n''')
            for wpt in self.waypoints:
                file.write(
wpt.getName().strip() + '''
SOME NUMBER (HAVENT FIGURED OUT YET BUT ITS SOMETHING BETWEEN 2 AND 5 APPARENTLY)
DCT
1 ''' + wpt.getCoords().strip() + ''' 0
0
0
0\n\n''')
            file.write(self.end[0:-1] + '''
1
-
1 COORDINATES HERE AND HEIGHT
-----
0
0

1
HEIGHT OF ARPT IN FT
-
-1000000
-1000000\n''')
            file.close()


#represents waypoint in .rte route
class RoutepointRTE():
    def __init__(self, name, airway, coords):
        self.name = name
        self.airway = airway
        self.coords = coords

    def getName(self):
        return self.name

    def getAirway(self):
        return self.airway

    def getCoords(self):
        return self.coords

#represents waypoint in .flp route
class RoutepointFLP():
    def __init__(self, name, coords):
        self.name = name
        self.coords = coords
    
    def getName(self):
        return self.name

    def getCoords(self):
        return self.coords

    def getAirway(self):
        return "DIRECT"     # make enum

#read the .flp flight plan
def readAerosoft(flp):
    aerosoft_flp = RouteFLP([], "", "")
    rte = []
    for line in flp:
        line.replace('\r', "")
        line.replace('\n', "")
        if line.startswith("ArptDep="):            
            aerosoft_flp.setStart(line.split("=")[1])
        elif line.startswith("ArptArr="):
            aerosoft_flp.setEnd(line.split("=")[1])
        elif line.startswith("DctWpt"):
            rte.append(line.split("=")[1])

    final_rte = []
    i = 0
    while i < len(rte):
        waypoint = RoutepointFLP(rte[i], rte[i+1])
        final_rte.append(waypoint)
        i += 2

    aerosoft_flp.setWaypoints(final_rte)

    return aerosoft_flp

#read the .rte flight plan
def readPmdg(rte):
    pmdg_rte = RouteRTE([], "", "")
    _rte = []
    i = 0
    j = 0
    newblock = False
    for line in rte:
        if i == 4:
            line.replace('\r', "")
            line.replace('\n', "")
            pmdg_rte.setStart(line)
        elif i > 4:
            if line == "\n":
                newblock = True
                j = 0
            if newblock or j != 0:
                newblock = False
                if j == 1:
                    line.replace("\r", "")
                    line.replace("\n", "")
                    _rte.append(line)
                    j += 1
                if j == 5:
                    coords = ""
                    for k in range(0, len(line)):
                        if k == 0:
                            continue
                        elif k < len(line)-3:
                            coords += line[k]
                    _rte.append(coords)
                    j += 1
                else:
                    j += 1
        i += 1

    pmdg_rte.setEnd(_rte[-4])

    final_rte = []
    x = 2
    while x < len(_rte) - 4:
        waypoint = RoutepointRTE(_rte[x], "DIRECT", _rte[x+1])
        final_rte.append(waypoint)
        x += 2

    pmdg_rte.setWaypoints(final_rte)

    return pmdg_rte

#convert from rte to flp
def convertRF(rte):
    new_flp = RouteFLP([], "", "")
    new_flp_rte = []
    new_flp.setStart(rte.getStart())
    new_flp.setEnd(rte.getEnd())
    for wpt in rte.getWaypoints():
        waypoint_lis = [x for x in wpt.getCoords().split(" ")]
        waypoint_lat = waypoint_lis[2] if waypoint_lis[1] == "N" else -1 * float(waypoint_lis[2]) 
        waypoint_long = waypoint_lis[4] if waypoint_lis[3] == "E" else -1 * float(waypoint_lis[4]) 
        waypoint_name = wpt.getName()
        new_flp_rte.append(RoutepointFLP(waypoint_name, str(waypoint_lat)+","+str(waypoint_long)))
    new_flp.setWaypoints(new_flp_rte)       
    return new_flp

#convert from flp to rte
def convertFR(flp):
    new_rte = RouteRTE([], "", "")
    new_rte_rte = []
    new_rte.setStart(flp.getStart())
    new_rte.setEnd(flp.getEnd())
    for wpt in flp.getWaypoints():
        waypoint_co = wpt.getCoords().split(",")
        waypoint_name = wpt.getName()
        waypoint_long = "E " + waypoint_co[1] if float(waypoint_co[1]) > 0 else "W " + waypoint_co[1]  
        waypoint_lat = "N " + waypoint_co[0] if float(waypoint_co[0]) > 0 else "S " + waypoint_co[0]
        new_rte_rte.append(RoutepointRTE(waypoint_name, "DIRECT", waypoint_lat + " " + waypoint_long))
    new_rte.setWaypoints(new_rte_rte)
    return new_rte

#main function
def main():
    #default output is stdout
    store_loc = "stdout"
    args = processArgs()
    #if script should write to a file
    if args.filenames != None:
        filename = args.filenames[0]
        rte = open(filename, "r")
        if filename.endswith(".rte"):
            Route = readPmdg(rte)
            Flp_route = convertRF(Route)
            Flp_route.printRte(args.filenames[1])       #print to given folder
        elif filename.endswith(".flp"):
            Route = readAerosoft(rte)
            Rte_route = convertFR(Route)
            Rte_route.printRte(args.filenames[1])       #print to given folder
        else:
            sys.exit("Invalid File")
    #if script should write to stdout
    elif args.filename != None:
        filename = args.filename
        rte = open(filename, "r")
        if filename.endswith(".rte"):
            Route = readPmdg(rte)
            Flp_route = convertRF(Route)
            Flp_route.printRte(store_loc)
            plotRoute(Route)
        elif filename.endswith(".flp"):
            Route = readAerosoft(rte)
            Rte_route = convertFR(Route)
            Rte_route.printRte(store_loc)
            plotRoute(Route)
        else:
            sys.exit("Invalid File")

#process command line arguments 
def processArgs():
    parser = ArgumentParser()
    parser.add_argument("-f", nargs=2, dest="filenames",metavar="FILES")
    parser.add_argument("-o", dest="filename")
    args = parser.parse_args()
    return args

#main function call
if __name__ == "__main__":
    main()
