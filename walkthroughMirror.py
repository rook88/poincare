from collections import defaultdict
import numpy as np
import cv2
import imageio

import poincare

theta = np.sqrt(5) * 0.5  - 0.5

colors = [
    (255, 255, 255)
    ,(255, 255, 127)
    ,(255, 255, 0)
    ,(255, 170, 0)
    ,(255, 90, 0)
    ,(255, 0, 0)
    ,(155, 0, 0)
    ,(100, 0, 0)
    ,(60, 0, 0)
    ,(40, 0, 0)
    ,(30, 0, 0)
    ,(20, 0, 0)
    ,(10, 0, 0)
    ,(5, 0, 0)
]

o = 0.0 + 0.0j

#pImg.drawEdge()

def drawAllCircles(label):
    pImg = poincare.poincareImg(radius = 3000, size = (4000, 4000))
    for c in [c for c in allCircles if c.isLine() or c.radius < 10]:
        try:
            pImg.drawCircle(c, c.color, thickness = 6)
        except:
            print "not drawn", c
#    img = pImg.getImg(hasMask = False, resize = (800, 800))
    img = pImg.getImg(hasMask = False)
    img = cv2.GaussianBlur(img, (5, 5), 5, 5)
    img = cv2.resize(img, dsize = (800, 800))
#    print "circles count = {}".format(len(allCircles))
    if poincare.testMode:
        cv2.imshow('myImg', img)
        cv2.imwrite('last.jpg', img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()
    if poincare.imagePath:
        cv2.imwrite(poincare.imagePath + '/' + label + '.jpg', img)
    return len(allCircles)

def genInitCirclesOLD(angleA, angleB, offset = 0.0):
    l1 = poincare.circle(somePoint = 0, someDirection = 1j, inverseRadius = 0.0)
    l2 = poincare.circle(somePoint = 0, someDirection = 1, inverseRadius = 0.0)
    directionA = np.exp(np.pi * 1j * angleA)
    directionB = 1j / np.exp(np.pi * 1j * angleB)

    pointA = 0.1j * (np.cos(np.pi * angleA) + np.sin(np.pi * angleB))
    pointB = 0.1 * (np.cos(np.pi * angleB) + np.sin(np.pi * angleA))

    la = poincare.circle(somePoint = pointA, someDirection = directionA, inverseRadius = 0.0)
    lb = poincare.circle(somePoint = pointB, someDirection = directionB, inverseRadius = 0.0)

    pointC = poincare.intersection(la, lb).z + offset
#    print pointA, pointB, pointC

    c1 = poincare.circle(center = pointC, radius = abs(pointA - pointC))
    c2 = poincare.getInverseCircle(c1, l1)
    c3 = poincare.getInverseCircle(c1, l2)
    c4 = poincare.getInverseCircle(c2, l2)
    circles = [c1, c2, c3, c4]
#    circles = [l1, l2, c1, c2, c3, c4]
    for c in circles:
        c.color = colors[0]
        c.depth = 1
#        print c
    return circles


def genInitCircles(angleA, angleB, offset = 0.0, zoom = 0.1):
    ret = []
    directionB = np.exp(np.pi * 1j * angleB)
    for i in range(int(1 / angleA + 0.5)):
        directionA1 = np.exp(i * np.pi * 2j * angleA)
        directionA2 = np.exp((i + 1) * np.pi * 2j * angleA)
#        line = poincare.circle(somePoint = 0, someDirection = directionA , inverseRadius = 0.0)
        pointA1 = directionA1 * zoom
        pointA2 = directionA2 * zoom
        directionC1 = directionA1 / directionB * 1j
        directionC2 = directionA2 * directionB / 1j
        la = poincare.circle(somePoint = pointA1, someDirection = directionC1, inverseRadius = 0.0)
        lb = poincare.circle(somePoint = pointA2, someDirection = directionC2, inverseRadius = 0.0)
        pointC = poincare.intersection(la, lb).z + offset
        c1 = poincare.circle(center = pointC, radius = abs(pointA1 - pointC))
#        print "test directions", directionC1, directionC2
#        print "test points", pointA1, pointA2, pointC
        ret.append(c1)
    for circle in ret:
        circle.color = colors[0]
        circle.depth = 1
    return ret
"""

    pointA = 0.1j * (np.cos(np.pi * angleA) + np.sin(np.pi * angleB))
    pointB = 0.1 * (np.cos(np.pi * angleB) + np.sin(np.pi * angleA))



    c2 = poincare.getInverseCircle(c1, l1)
    c3 = poincare.getInverseCircle(c1, l2)
    c4 = poincare.getInverseCircle(c2, l2)
    circles = [c1, c2, c3, c4]
#    circles = [l1, l2, c1, c2, c3, c4]
    for c in circles:
        c.color = colors[0]
        c.depth = 1
#        print c
"""


def genCirclesIter(depth = 1, minRadius = 0.0, maxRadius = 1.7):
    circles = allCircles[:]
    for c1 in circles:
        for c2 in circles:
            if c1 <> c2 and (not c1.isLine() or not c2.isLine()):
                c3 = poincare.getInverseCircle(c1, c2)
                if c3.radius > minRadius and c3.radius < maxRadius and not c3.getKey() in allCirclesKeys:
                    c3.depth = c1.depth + c2.depth
                    c3.color = colors[c3.depth - 1]
                    allCircles.append(c3)
                    allCirclesKeys[c3.getKey()] += 1

def genCircles(depth = 1):
    for i in range(depth):
        genCirclesIter(i, 0.001)

allCircles = []
allCirclesKeys = defaultdict(int)

def genImg(label, depth, angleA, angleB, offset, zoom):
    global allCircles, allCirclesKeys
    allCircles = genInitCircles(angleA, angleB, offset, zoom)
    allCirclesKeys = defaultdict(int)
    genCircles(depth)
    allCircles.reverse()
    return drawAllCircles(label)


i = 0
timeFrameNow = poincare.zoom
while True:
    i += 1
    timeFrame = (1 + np.sin(timeFrameNow * np.pi - np.pi / 2)) / 2
    label = str(timeFrameNow)
#    timeFrame = (1 + np.sin(timeFrame * np.pi - np.pi / 2)) / 2
#    if i > 99:
#        break
    angleA = 1 / 4.0
    angleB = 1 / (4.0 + 0.01 + timeFrame * 1.99)
    offset = 0
    zoom = 0.0001 + timeFrame * 0.3
#    angleB = 1 / 7.0
#    offset = np.exp(np.pi * 2j * timeFrame) - 1
#    offset *= 0.1
    count = genImg(label, poincare.depth, angleA, angleB, offset, zoom)
    print "frameNumber = {} count = {} frameName = {} timeFrame = {} angleA = {} angleB = {}, offset = {}".format(i + 1, count, label, timeFrame, angleA, angleB, offset)
#    roiOut = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    timeFrameNow = ( timeFrameNow + (np.sqrt(5) - 1) / 2) % 1  

exit(0)

#offset *= 8009

angleB = 1 / 5.01
#offset = 0.01 + 0.01j
genImg(angleA, angleB, offset, test = False)
