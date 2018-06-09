import numpy as np
import cv2

import poincare
import random
import copy

p = 3
q = 7

zerolabels = [i + 1 for i in range(p)]

t1 = 1 - np.tan(np.pi / p) * np.tan(np.pi / q)
t2 = 1 + np.tan(np.pi / p) * np.tan(np.pi / q)

gonRadius = np.sqrt(t1 / t2)

pImg = poincare.poincareImg(radius = 900, pointRadius = 5, size = [2000, 2000])
#pImg.drawEdge()

gonFundamental = poincare.polygon(poincare.origin, verticeCount = 5, radius = gonRadius)

gons = {}

class gonClass():
    def __init__(self, p, q, r, path):
        self.path = path
        label = "-".join([str(d) for d in path])
        self.label = label
        self.color = colorFromPath(self.path)
        if label == "":
            self.gon = poincare.polygon(poincare.origin, verticeCount = p, radius = r)
        else:
            if label in gons:
                self.gon = copy.copy(gons[label]).gon
            else:
                gonIter = gonClass(p, q, r, path[1:])
                self.gon = gonIter.gon.getMirror(int(path[0]))
    def __str__(self):
        ret = "Gon, label = {}, polygon = {}".format(self.label, self.gon)
        return ret

def getGon(p, q, r, label):
    if label == []:
        return poincare.polygon(poincare.origin, verticeCount = p, radius = r)
    else:
        iter = getGon(p, q, r, label[1:])
        return iter.getMirror(int(label[0]))

theta = 1.5 - np.sqrt(5) * 0.5 

def colorFromLabel(label):
    hue = int(len(label) * theta * 180) % 180
    return (hue, 255, 255)

def colorFromPath2(path):
    hue = 0.0
    delta = 1.0 / (p + 1)
    for direction in path:
        hue += direction * delta * 180
        delta *= theta
    hue = int(hue) % 180
    return (hue, 255, 255)

def colorFromPath(path):
    hue = 0.0
    delta = 1.0 / p 
    for direction in list(reversed(path)):
        hue += (direction - 2) * delta * 180
        delta /= p
    hue = int(hue) % 180
    if path:
        value = 255 * (3.0 / (2.0 + len(path)))
        saturation = 255
    else:
        value = 255
        saturation = 0
    return (hue, saturation, value)
    

centers = []

def isNewGon(gNew):
    if abs(gNew.gon.center.z) > 0.9999:
        return False
    for label in gons:
        if label <> gNew.label:
            gOld = gons[label]
            if abs(gNew.gon.center.z - gOld.gon.center.z) < 0.00001:
                return False
    return True

def iterLabel(label):
    temp = gonClass(p, q, gonRadius, label)
    gons[str(label)] = temp
    gonTemp = temp.gon
    gonColor = colorFromLabel(label)
    if isNewGon(temp):
        print("New: {}".format(temp))
        pImg.drawPolygon(gonTemp, color = gonColor)
        for zerolabel in zerolabels:
            if label:
                nextLabelItem = (zerolabel + label[-1] - 1) % p + 1
            else:
                nextLabelItem = zerolabel
            newLabel = label + [nextLabelItem]
            iterLabel(newLabel)
    else:
        print("Old: {}".format(temp))


def iterLabels(n):
    generation = [gons[l] for l in gons if len(gons[l].path) == n]
    generation = [g for g in gonsTable if len(g.path) == n]
    for gOld in generation:
        for zerolabel in zerolabels:
            if gOld.path:
                nextLabelItem = (zerolabel + gOld.path[-1] - 1) % p + 1
                nextLabelItem = zerolabel
            else:
                nextLabelItem = zerolabel
            newPath = gOld.path + [nextLabelItem]
            temp = gonClass(p, q, gonRadius, newPath)
            gonColor = colorFromPath(temp.path)
            if isNewGon(temp):
                gons[temp.label] = temp
                gonsTable.append(temp)
#                print("New: {}".format(temp))
#                pImg.drawPolygon(temp.gon, color = gonColor)
            else:
                pass
#                print("Old: {}".format(temp))

gons[""] = gonClass(p, q, gonRadius, [])
gonsTable = [gonClass(p, q, gonRadius, [])]

#iterLabel([])
iterLabels(0)
iterLabels(1)
iterLabels(2)
iterLabels(3)
#iterLabels(4)
#iterLabels(5)

print gons.keys()

multiplier = 14.2
multiplier = 1.0

def showImg():
    img = pImg.getImg(multiplier = multiplier)
    img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    img = cv2.blur(img, (4, 4))
    img = cv2.resize(img, dsize = (800, 800))
    cv2.imshow('myImg', img)
    cv2.imwrite("lastPolygon.jpg", img)
    cv2.waitKey(0)


for gon in gonsTable:
#    gon = gons[label]
    gonNew = getGon(p, q, gonRadius / multiplier, gon.path)
    print gon, gonNew, gon.color
    if gon.label in ["", "1", "2-1", "1-2-1"] or 1 == 1:
        pImg.drawPolygon(gonNew, color = gon.color, offset = multiplier)
        showImg()
