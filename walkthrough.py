import numpy as np
import cv2

import poincare

theta = np.sqrt(5) * 0.5  - 0.5

o = 0.0 + 0.0j

pImg = poincare.poincareImg(radius = 400)
pImg.drawEdge()

#move = lambda z: z * np.exp(0.75 * np.pi * 2j) + 0.05  
#move = lambda z: z * np.exp(0.63 * np.pi * 2j) + 0.05  
move = lambda z: z * np.exp(theta * np.pi * 2j)

def genLines(points):
    ret = []
    for a in points:
        aInv = a.getInverse()
        b = poincare.exteriorPoint(0.5 * (a.z + aInv.z))
        l = poincare.circle(somePoint = b.z, someDirection = b.z * 1j, inverseRadius = 0.0)
        ret.append(l)
    return ret

def drawImg():
    for n in range(7):
        p1 = points[0 + n]
        l1 = lines[0 + n]
        l2 = lines[1 + n]
        b = poincare.intersection(l1, l2)
        c = poincare.circle(center = b.z, radius = abs(b.z - p1.z))
        print b, p1
        pImg.drawPoint(p1)
        pImg.drawCircle(c)

points = []
a = poincare.interiorPoint(0.5)
for i in range(8):
    points.append(a.getCopy())
    a.map(move)

toPoint = poincare.interiorPoint(0.02 + 0.01j)
map = poincare.isometry(0, toPoint)

for i in range(10):
    lines = genLines(points)
    drawImg()
    for point in points:
        point.map(map.map)

#c = poincare.circle(somePoint = 0.5 + 0.5j, someDirection = 1, inverseRadius = 1.3)
c = poincare.circle()
#l1 = poincare.circle(somePoint = 1.0 + 0.5j, someDirection = 1, inverseRadius = 0.0)
#l2 = poincare.circle(somePoint = 2.0 + 1.0j, someDirection = 1 + 1j, inverseRadius = 0.0)
pImg.drawCircle(c)
#pImg.drawCircle(l1)
#pImg.drawCircle(l2)
#b = poincare.intersection(l1, l2)


img = pImg.getImg()

cv2.imshow('myImg', img)
cv2.waitKey(0)


