import numpy as np
import cv2

import poincare
import random
import copy
import imageio

class gonClass():
    def __init__(self, p, q, r, path):
        self.path = path
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
        self.color = colorFromZ(self.gon.center.z, self.path)
#        self.color = colorFromPath(self.path)
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

def colorFromPath3(z, path, weight):
    (hue1, saturation1, value1) = colorFromZ(z, path)
    value2 = 1 + ((len(path) + 2) % 3) * 127
    saturation = int(weight * saturation1)
    value = int(weight * value1 + (1 - weight) * value2)
    hue = hue1
    return (hue, saturation, value)


def colorFromPath(path):
    hue = 0.0
    delta = 1.0 / p 
    for direction in list(reversed(path)):
        hue += (direction - 2) * delta * 180
        delta /= p 
    hue = int(hue) % 180
    if path:
        value = int(255 * (3.0 / (2.0 + len(path))))
        saturation = 255
    else:
        value = 255
        saturation = 0
    return (hue, saturation, value)
    
def colorFromZ(z, path):
    hue = int(np.imag(np.log(z)) / np.pi * 90) % 180
    print z, hue
    if path:
        value = int(255 * (3.0 / (2.0 + len(path))))
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
            if abs(gNew.gon.center.z - gOld.gon.center.z) < 0.001:
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
#            gonColor = colorFromPath(temp.path)
#            gonColor = colorFromZ(temp.gon.center.z, temp.path)
            if isNewGon(temp):
                gons[temp.label] = temp
                gonsTable.append(temp)
#                print("New: {}".format(temp))
#                pImg.drawPolygon(temp.gon, color = gonColor)
            else:
                pass
#                print("Old: {}".format(temp))

def showImg(pImg):
    img = getImg(pImg)
    cv2.imshow('myImg', img)
    cv2.imwrite("lastPolygon.jpg", img)
    cv2.waitKey(0)

def getImg(pImg, color = "rgb"):
    multiplier = pImg.multiplier
    img = pImg.getImg(multiplier = multiplier)
    if color == "rgb":
        img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
    if color == "bgr":
        img = cv2.cvtColor(img, cv2.COLOR_HSV2BGR)
    img[np.where((img == [0,0,0]).all(axis = 2))] = [255,255,255]
    img = cv2.blur(img, (4, 4))
    img = cv2.resize(img, dsize = (800, 800))
    return img

def iterImg(multiplier = 1.0):
    pImg = poincare.poincareImg(radius = 900, pointRadius = 5, size = [2000, 2000], backgroundIsWhite = True)
    pImg.multiplier = multiplier
#    if gon.label in ["", "1", "1-2", "1-2-3", "1-2-3-1", "1-2-3-1-2"] or 1 == 0:
    for gon in gonsTable:
#    gon = gons[label]
        gonNew = getGon(p, q, gonRadius / multiplier, gon.path)
        if gon.label == "1-2-3-1" or 1 == 1:
            color = gon.color
            color = colorFromPath3(gon.gon.center.z, gon.path, 1.0 / multiplier / multiplier)
            print gon, gonNew, gon.color, color
            pImg.drawPolygon(gonNew, color = color, offset = multiplier)
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
gonsTable = [gonClass(p, q, gonRadius, [])]


depth = poincare.depth
for i in range(depth):
    iterLabels(i)

#print gons.keys()
gonsTable.sort(key = lambda x: x.label)
print [g.label for g in gonsTable]

ims = []

frameCount = poincare.frameCount

mpInit = 10.0 ** (1.0 / frameCount)
ts = np.linspace(0.0, 1.0, frameCount)
ts = [(1.0 + n) / frameCount for n in range(frameCount)]

print ts

if poincare.multiplier:
    mps = [poincare.multiplier]
else:
    mps = [np.sqrt(1 / t) for t in ts]

print mps


#exit(0)

frameN = 0
for mp in mps:
    frameN += 1
    print "frame {}".format(frameN)
    pImg = iterImg(mp)
    if poincare.testMode:
        showImg(pImg)
    if poincare.outputFile:
        ims.append(getImg(pImg, color = "bgr"))


if poincare.outputFile:
    ims += list(reversed(ims))
    imageio.mimwrite(uri = poincare.outputFile, ims = ims, macro_block_size = None, fps = 24)

