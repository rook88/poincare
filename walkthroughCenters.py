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
 
def showImg(pImg, f = 1.0):
    img = getImg(pImg, f = f)
    cv2.imshow('myImg', img)
    cv2.waitKey(0)


def saveImg(pImg, outputFile = "lastPolygon.jpg"):
    img = getImg(pImg)
    print "Saved file {}".format(outputFile)
    cv2.imwrite(outputFile, img)

def getImg(pImg, color = "rgb", f = 1.0):
    multiplier = pImg.multiplier
    img = pImg.getImg(multiplier = multiplier)
    if color == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    if color == "bgr":
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img[np.where((img == [0,0,0]).all(axis = 2))] = [255,255,255]
    img = cv2.blur(img, (4, 4))
    img = cv2.resize(img, dsize = (1600, 1600))
    return img

def iterImg(multiplier = 1.0, reverse = False, radiusFactor = 1.0):
    radius = int(3200 * radiusFactor)
    pImg = poincare.poincareImg(radius = radius, pointRadius = 5, size = [6400, 6400], backgroundIsWhite = True)
    pImg.multiplier = multiplier
    if reverse:
        tempTable = reversed(gonsTable)
    else:
        tempTable = gonsTable
    for gon in tempTable:
        gonNew = getGon(p, q, gonRadius / multiplier, gon.path)
        if multiplier < 1:
            w = 1.0
        else:
            w = 1.0 / multiplier / multiplier
        color = (0, 0, 208)
        pImg.drawPolygonVertices(gonNew, color = color, offset = multiplier)
    return pImg



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

gonsTable = [gons[l] for l in gons]
gonsTable.sort(key = lambda x: x.direction)
#print [g.label for g in gonsTable]

depths = {} 
for g in gonsTable:
    if g.depth in depths:
        depths[g.depth] += 1
    else:
        depths[g.depth] = 1


def depthStr(depths):
    str = "1,"
    for i in range(depth):
        dCur = depths[i + 1]
        dPrev = float(depths[i])
#        print "{:>8} {:>8} {:>8}     {:>8.6f}".format(i + 1, dCur, dCur / p, dCur / dPrev)
        str += "{},".format(dCur)
    str = "{:>9.7f},{}".format(dCur / dPrev, str) 
    return str

print "{},{},{}".format(p, q, depthStr(depths))
    
zoomFactor = poincare.zoom

#exit(0)

pImg = iterImg()
print poincare.outputFile
showImg(pImg)
if poincare.outputFile:
    saveImg(pImg, poincare.outputFile)


