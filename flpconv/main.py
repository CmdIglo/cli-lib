
import sys

#represents a .flp flight plan
class RouteFLP():
    def __init__(self, waypoints, start, end, rwydep, rwyarr, sid, star):
        self.waypoints = waypoints
        self.start = start
        self.end = end
        self.rwydep = rwydep
        self.rwyarr = rwyarr
        self.sid = sid
        self.star = star

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

    def getRwyDep(self):
        return self.rwydep

    def setRwyDep(self, rwy):
        self.rwydep = rwy

    def getRwyArr(self):
        return self.rwyarr

    def setRwyArr(self, rwy):
        self.rwyarr = rwy

    def getSid(self):
        return self.sid

    def setSid(self, sid):
        self.sid = sid

    def getStar(self):
        return self.star

    def setStar(self, star):
        self.star = star

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
    aerosoft_flp = RouteFLP([], "", "", "", "", "", "")
    rte = []
    for line in flp:
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

    print(final_rte)

#read the .rte flight plan
def readPmdg(rte):
    pass

#convert from rte to flp
def convertRF(rte, flp):
    pass

#convert from flp to rte
def convertFR(flp, rte):
    pass

#get flight plan
def getInput():
    file_name = input("File Name: ")
    route = open(file_name, "r")
    return (file_name, route)

#main function
def main():
    filename, rte = getInput()
    if filename.endswith(".rte"):
        readPmdg(rte)
    elif filename.endswith(".flp"):
        readAerosoft(rte)
    else:
        sys.exit("Invalid File")

#main function call
if __name__ == "__main__":
    main()

