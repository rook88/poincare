import numpy as np
import cv2
import imageio

import poincare


origin = 0.0 + 0.0j

#pImg.drawEdge()

goldenRatio = 0.5 * (np.sqrt(5) + 1)

def genLines(points):
    ret = []
    for a in points:
        aInv = a.getInverse()
        b = poincare.exteriorPoint(0.5 * (a.z + aInv.z))
        l = poincare.circle(somePoint = b.z, someDirection = b.z * 1j, inverseRadius = 0.0)
        ret.append(l)
    return ret

def genImg(offset = 0.0, theta = np.pi * 2 / 14, r = 0.5, depth = 5):
    pointKeys = {}
    pImg = poincare.poincareImg(size = [4800, 4800], radius = 2000, pointRadius = 4, pointColor = (255, 255, 0))
    ind = 0
    allPoints = [poincare.interiorPoint(origin)]
    for iterRound in range(depth):
        curPoints = list(allPoints)
#        print("iter {}/{}, points = {}".format(iterRound + 1, depth, len(curPoints)))
        for i in range(7):
            ind += 1
            j = int(goldenRatio * ind)
            j = ind
            genPoint = poincare.interiorPoint(r * np.exp(2 * j * theta * 1j))
            if iterRound % 2 == 0:
                isometry = poincare.isometry(fromPoint = 0, toPoint = genPoint)
            else:
                isometry = poincare.isometry(fromPoint = 0, toPoint = genPoint.getMirror())
            for point in curPoints:
                newPoint = point.getMapped(isometry.map)
                if newPoint.key in pointKeys:
                    pass
                else:
                    allPoints.append(newPoint)
                    pointKeys[newPoint.key] = 1
    isometry = poincare.isometry(fromPoint = 0, toPoint = poincare.interiorPoint(offset))
    for p in allPoints:
        pImg.drawPoint(p.getMapped(isometry.map))

    img = pImg.getImg()
    img = cv2.blur(img, (5, 5))
    img = cv2.resize(img, (960, 960))

    return img

theta = np.pi * 2 / 14
t1 = np.tan(theta)
t2 = np.tan(np.pi / 2 - theta * 2)
r = np.sqrt((t2 - t1) / (t1 + t2))

print t1, t2, r
#theta = theta + 0.0005
#r = r + 0.01
offset = 0.1
depth = 5

ims = []

def genOffset(n, k):
    def ret(t):
        if t * 2 * n  <  k:
            return 0
        if t * 2 * n  <  k + 1:
            return t * 2 * n  -  k
        if t * 2 * n  <  k + n:
            return 1
        if t * 2 * n  <  k + n + 1:
            return k + n + 1 - t * 2 * n  
        return 0
    return ret

offsetRadius = genOffset(2, 0)
offsetTheta = genOffset(2, 1)
        
frameCount = 25
for frameNumber in range(frameCount):
#    t = (1.0 * frameNumber / frameCount - 2.0 / frameCount ) % 1
    t = 1.0 * frameNumber / frameCount 
    currentTheta = theta + offsetTheta(t) * 0.0005
    currentRadius = r + offsetRadius(t) * 0.01
    offset = 0.2 + 0.2 * np.exp(np.pi * 2 * 1j * t)
    print frameNumber
    img = genImg(offset = offset, theta = currentTheta, r = currentRadius, depth = depth)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
    ims.append(img)

#    cv2.imshow('myImg', img)
#    cv2.waitKey(0)

imageio.mimwrite(uri = "wt37.mp4", ims = ims, fps = 25)
cv2.imwrite("last.jpg", img)


