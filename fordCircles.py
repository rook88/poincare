import numpy as np

class rational():
    def __init__(self, a, b):
        self.a = a
        self.b = b
    def __str__(self):
        return "{}/{}".format(self.a, self.b)
    def addFarey(self, other):
        return rational(self.a + other.a, self.b + other.b)
    def __eq__(self, other):
        return (self.a * other.b == self.b * other.a)
    def __ne__(self, other):
        return not (self == other)
    def __lt__(self, other):
        return (self.a * other.b < self.b * other.a)
    def asFloat(self):
        return 1.0 * self.a / self.b
    def __sub__(self, other):
        return rational(self.a * other.b - self.b * other.a, self.b * other.b)
    def getValues(self, radius = 1.0):
        angle = np.pi * 2 * self.a / self.b
        chord = 2 * radius * np.sin(angle / 2)
        halfChord = 2 * radius * np.sin(angle / 4)
        radiusOut = radius * np.tan(angle / 2)
        inverseSagitta = radius * (np.sqrt(1 + (np.tan(angle / 2)) ** 2) - 1)
        frmString = "{:6.1f} " * 4
        return frmString.format(chord, halfChord, radiusOut, inverseSagitta)
        #        return angle, chord, halfChord, radius, inverseSagitta

        
class pair():
    def __init__(self, start, end, level = 1):
        self.start = start
        self.end = end
        self.level = level
    def __str__(self):
        return "{}_{}".format(self.start, self.end)
    def __abs__(self):
        return (self.end - self.start).asFloat()
    def split(self):
        middle = self.start.addFarey(self.end)
        ret1 = pair(self.start, middle, self.level + 1)
        ret2 = pair(middle, self.end, self.level + 1)
        return ret1, ret2
    def getValues(self, radius = 1.0):
        return (self.end - self.start).getValues(radius)
        
def iterEndPoints(points):
    ret = []
    for i in range(len(points) - 1):
        ret.append(points[i].addFarey(points[i + 1]))
    return ret

initPairs = [pair(rational(0, 1), rational(1, 1))]
iterPairs = initPairs[:]
allPairs = initPairs[:]

diskRadius = 106.0
minLength = 20.0 / diskRadius / 2 / np.pi

for i in range(9):
    nextPairs = []
    for p in iterPairs:
        p1, p2 = p.split()
        if abs(p1) > minLength and abs(p2) > minLength:
            nextPairs.append(p1)
            nextPairs.append(p2)
    allPairs += nextPairs
    iterPairs = nextPairs[:]


arcs = {}
for p in allPairs:
    key = abs(p)
    if not key in arcs:
        arcs[key] = type('arc', (), {})()
        arcs[key].items = []
    arcs[key].info = p.getValues(diskRadius)
    arcs[key].items.append(p)
    
for key in reversed(sorted(arcs.keys()[:])):
    if key < 0.5:
        printLine = arcs[key].info
        for p in arcs[key].items:
            printLine += " " + str(p) 
        print(printLine)
        
#print (rational(1, 1) == rational(1, 1))
#print (rational(0, 1) == rational(1, 1))
#r = rational(0, 1)
#print(r)

