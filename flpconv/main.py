
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

    def printRte(self, stream):
        if stream == "stdout":
            for wpt in self.waypoints:
                print("Waypoint:" + wpt.getName() + "At:" + wpt.getCoords())
        else:
            pass

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

    def printRte(self, stream):
        if stream == "stdout":
            for wpt in self.waypoints:
                print("Waypoint:" + wpt.getName() + "At:" + wpt.getCoords())
        else:
            pass


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
            pmdg_rte.setStart(line)
        elif i > 4:
            if line == "\n":
                newblock = True
                j = 0
            if newblock or j != 0:
                newblock = False
                if j == 1:
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

    pmdg_rte.setEnd(_rte[-2])

    final_rte = []
    x = 2
    while x < len(_rte) - 2:
        waypoint = RoutepointRTE(_rte[x], "DIRECT", _rte[x+1])
        final_rte.append(waypoint)
        x += 2

    pmdg_rte.setWaypoints(final_rte)

    return pmdg_rte

#convert from rte to flp
def convertRF(rte):
    new_flp = RouteFLP([], "", "", "", "", "", "")
    new_flp_rte = []
    new_flp.setStart(rte.getStart())
    new_flp.setEnd(rte.getEnd())
    for wpt in rte.getWaypoints():
        pass
    pass

#convert from flp to rte
def convertFR(flp):
    new_rte = RouteRTE([], "", "")
    new_rte_rte = []
    new_rte.setStart(flp.getStart())
    new_rte.setEnd(flp.getEnd())
    for wpt in flp.getWaypoints():
        waypoint = RoutepointRTE(wpt.getName(), "DIRECT", wpt.getCoords().replace(",", " ", 1))
        new_rte_rte.append(waypoint)
    return new_rte

#get flight plan
def getInput():
    file_name = input("File Name: ")
    store_loc = input("Store in: ")
    route = open(file_name, "r")
    return (file_name, route, store_loc)

#main function
def main():
    filename, rte, store_loc = getInput()
    store_loc = "stdout"
    if filename.endswith(".rte"):
        Route = readPmdg(rte)
        Route.printRte(store_loc)
    elif filename.endswith(".flp"):
        Route = readAerosoft(rte)
        Route.printRte(store_loc)
    else:
        sys.exit("Invalid File")

#main function call
if __name__ == "__main__":
    main()

