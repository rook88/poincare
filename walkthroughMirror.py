import numpy as np
import cv2

import poincare

theta = np.sqrt(5) * 0.5  - 0.5

o = 0.0 + 0.0j

pImg = poincare.poincareImg(radius = 400)
#pImg.drawEdge()

l1 = poincare.circle(somePoint = 0, someDirection = 1j, inverseRadius = 0.0)
l2 = poincare.circle(somePoint = 0, someDirection = 1, inverseRadius = 0.0)
c = poincare.genCircleFromPoints(0.03 + 0.03j, 0.7, 0.7j)
#c = poincare.circle(center = 0.1 + 0.1j, radius = 0.2)
circles = [l1, l2, c]
allCircles = [l1, l2, c]

#c2 = poincare.getInverseCircle(c, l1)
#circles.append(c2)

def genCircles():
    circles = allCircles[:]
    for c1 in circles:
        for c2 in circles:
            if c1 <> c2 and (not c1.isLine() or not c2.isLine()):
#                print c1, c2
                c3 = poincare.getInverseCircle(c1, c2)
                allCircles.append(c3)

genCircles()
genCircles()
#genCircles()


for c in allCircles:
    try:
        pImg.drawCircle(c)
    except:
        print "not drawn", c
#    print c.getSomePoints()
            


toPoint = poincare.interiorPoint(0.02 + 0.01j)

img = pImg.getImg(hasMask = False)

cv2.imshow('myImg', img)
cv2.waitKey(0)


