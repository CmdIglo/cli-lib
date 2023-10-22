
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

#represents a .rte flight plan
class RouteRTE():
    def __init__(self, waypoints, start, end):
        self.waypoints = waypoints
        self.start = start
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
def readAerosoft():
    pass

#read the .rte flight plan
def readPmdg():
    pass

#convert from rte to flp
def convertRF(rte, flp):
    pass

#convert from flp to rte
def convertFR(flp, rte):
    pass

#main function
def main():
    rte = RouteRTE("waypoints", "EDDH", "LSZH")
    flp = RouteFLP("waypoints", "EDDH", "LSZH", 1, 2, "SID", "STAR")
    print("Jup, works")
    pass

#main function call
if __name__ == "__main__":
    main()

