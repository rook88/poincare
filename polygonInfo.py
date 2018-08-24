import numpy as np
import cv2

import poincare
import random
import copy

theta = 1.5 - np.sqrt(5) * 0.5 

class gonClass():
    def __init__(self, p, q, r, path):
        self.path = path
        self.depth = len(path)
        label = "-".join([str(d) for d in reversed(path)])
        self.label = label
        if label == "":
            self.gon = poincare.polygon(poincare.origin, verticeCount = p, radius = r)
        else:
            if label in gons:
                self.gon = copy.copy(gons[label]).gon
            else:
                gonIter = gonClass(p, q, r, path[1:])
                self.gon = gonIter.gon.getMirror(int(path[0]))
        self.color = (0, 0, 1)
        if path:
            d = path[0]
        else:
            d = 1
        self.direction = np.imag(np.log(self.gon.center.z ** p)) 
    def __str__(self):
        ret = "Gon, label = {}, polygon = {}, direction = {}".format(self.label, self.gon, self.direction)
        return ret

def getGon(p, q, r, label):
    if label == []:
        return poincare.polygon(poincare.origin, verticeCount = p, radius = r)
    else:
        iter = getGon(p, q, r, label[1:])
        return iter.getMirror(int(label[0]))
centers = []

def isNewGon(gNew):
    if abs(gNew.gon.center.z) > 0.999999:
        return False
    for label in gons:
        if label <> gNew.label:
            gOld = gons[label]
            if abs(gNew.gon.center.z - gOld.gon.center.z) < 0.0001:
                return False
    return True

def iterLabels(n):
    generation = [gons[l] for l in gons if len(gons[l].path) == n]
    generation.sort(key = lambda x: x.direction)
    for zerolabel in zerolabels:
        for gOld in generation:
            if gOld.path:
                nextLabelItem = (zerolabel + gOld.path[-1] - 1) % p + 1
#                nextLabelItem = zerolabel
            else:
                nextLabelItem = zerolabel
            newPath = gOld.path + [nextLabelItem]
            temp = gonClass(p, q, gonRadius, newPath)
            if isNewGon(temp):
                gons[temp.label] = temp
 
def iterImg(multiplier = 1.0, reverse = False, radiusFactor = 1.0):
    radius = int(3200 * radiusFactor)
    pImg = poincare.poincareImg(radius = radius, pointRadius = 5, size = [6400, 6400], backgroundIsWhite = True)
    tempTable = gonsTable
    for gon in tempTable:
        gonNew = getGon(p, q, gonRadius / multiplier, gon.path)
        circles = pImg.getPolygonGeneratingCircles(gonNew)
        for c in circles:
            allCircles[c.center] = c

p = poincare.p
q = poincare.q

zerolabels = [i + 1 for i in range(p)]

t1 = 1 - np.tan(np.pi / p) * np.tan(np.pi / q)
t2 = 1 + np.tan(np.pi / p) * np.tan(np.pi / q)

gonRadius = np.sqrt(t1 / t2)
gonFundamental = poincare.polygon(poincare.origin, verticeCount = 5, radius = gonRadius)
gons = {}
gons[""] = gonClass(p, q, gonRadius, [])

depth = poincare.depth
for i in range(depth):
    iterLabels(i)
    if len(gons) > 200:
        break
depth = i + 1
#    print [label for label in gons]

allCircles = {}
gonsTable = [gons[l] for l in gons]
gonsTable.sort(key = lambda x: x.direction)
#print [g.gon.center for g in gonsTable]

pImg = iterImg()

diskRadius = poincare.multiplier

verticeDistances = {} 
for g in gonsTable:
#    print g.gon
    for v in g.gon.vertices:
#        print v
        if v.r * diskRadius < diskRadius - 5.0:
            verticeDistances[int(np.round(v.r * diskRadius * 10, 0))] = 1
vDistances = [v / 10.0 for v in verticeDistances.keys()]
vDistances.sort()

mainAngle = 360.0 / p

groups = {}
for c in allCircles.values():
    if c.radius > 100.0:
        c.radius = 0.0
#    key = "{:4.1f}".format(c.radius * diskRadius)

    key = int(np.round(c.radius * diskRadius, 0))
    if key in groups:
        groups[key].append(c)
    else:
        groups[key] = [c]
#print groups

a = groups.keys()
a.sort()
a.reverse()


def rational(x):
    error = 2
    for b in [n + int(diskRadius) for n in range(int(diskRadius))]:
        a = np.round(x * b, 0)
        if abs(x - a / b) < error:
            error = abs(x - a / b)
            reta = a
            retb = b
    return (reta, retb)

def toFirstRadius(x):
    a = x / 180.0 * np.pi
    ret = np.sqrt(2 - 2 * np.cos(a)) * helpRadius
    return ret

if poincare.zoom > 1:
    helpRadius = poincare.zoom
else:
    helpRadius = groups[a[0]][0].radius

print "========================================================================"
print "p, q        = {},{}".format(p, q)
print "mainAngle   = {:>5.1f}".format(mainAngle)
print "diskRadius  = {:>5.1f}".format(diskRadius)
print "helpRadius = {:>5.1f}".format(helpRadius)
#print "firstAngle  = {:>5.1f}".format(firstAngle)
print "---- vertice distances -------------------------------------------------"
for vDistance in vDistances:
    print vDistance

for key in a:
    c = groups[key][0]
    if c.radius * diskRadius < 5.0 and c.radius > 0:
        continue
    print "-------------------------------------- dist = {:5.1f} radius = {:5.1f} -----".format(
        abs(c.center) * diskRadius
            ,c.radius * diskRadius
            )
#    for c in groups[key]:
#        print c, np.round(np.imag(np.log(c.center)), 9)  / np.pi * 180
    angles = [np.imag(np.log(c.center))  / np.pi * 180 for c in groups[key]]
#     print "1:", angles
    angles = [abs(a) for a in angles if abs(a) < mainAngle]
    angles = [abs(a - mainAngle / 2) for a in angles]
    angles = [round(a, 1) for a in angles]
#    print "2:", angles
    angles = list(set(angles))
    angles.sort()
    for angle in angles:
        tanAngle = np.tan(angle / 180 * np.pi)
        toFirst = toFirstRadius(angle)
        (a, b) = rational(tanAngle)
#        print "{:<6.1f} {:>6.1f} {:>6.4} = {} / {}".format(angle, toFirst, tanAngle, a, b)
        print "{:<6.1f} {:>6.1f}".format(angle, toFirst)        


