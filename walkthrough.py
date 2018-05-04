import numpy as np
import cv2

import poincare

theta = np.sqrt(5) * 0.5  - 0.5

o = 0.0 + 0.0j

pImg = poincare.poincareImg(radius = 100)
pImg.drawEdge()

move = lambda z: z * np.exp(0.75 * np.pi * 2j) + 0.05  
move = lambda z: z * np.exp(0.63 * np.pi * 2j) + 0.05  
move = lambda z: z * np.exp(theta * np.pi * 2j) + 0.05  

a = poincare.interiorPoint(0.5 + 0.5j)
for i in range(9):
    a.map(move)
    aInv = a.getInverse()
    pImg.drawPoint(a)
#    pImg.drawPoint(aInv)
#    print aInv.z
    a = aInv.getInverse()

c = poincare.circle(somePoint = 0.5 + 0.5j, someDirection = 1, inverseRadius = 1.3)
l1 = poincare.circle(somePoint = 1.0 + 0.5j, someDirection = 1, inverseRadius = 0.0)
l2 = poincare.circle(somePoint = 2.0 + 1.0j, someDirection = 1 + 1j, inverseRadius = 0.0)
pImg.drawCircle(c)
pImg.drawCircle(l1)
pImg.drawCircle(l2)
b = poincare.intersection(l1, l2)
pImg.drawPoint(b)


img = pImg.getImg()

cv2.imshow('myImg', img)
cv2.waitKey(0)


