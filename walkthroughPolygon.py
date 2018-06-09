import numpy as np
import cv2

import poincare
import random
import copy

p = 5
q = 4

t1 = 1 - np.tan(np.pi / p) * np.tan(np.pi / q)
t2 = 1 + np.tan(np.pi / p) * np.tan(np.pi / q)

gonRadius = np.sqrt(t1 / t2)
#print gonRadius


pImg = poincare.poincareImg(radius = 400, pointRadius = 5)
pImg.drawEdge()

origin = poincare.interiorPoint(0.0000 + 0.0000j)

#p1 = poincare.interiorPoint(0.5 + 0.0j)
#p2 = poincare.interiorPoint(0.4 + 0.3j)
#p3 = poincare.interiorPoint(0.3 + 0.3j)

gonFundamental = poincare.polygon(origin, verticeCount = 5, radius = gonRadius)

#print gon.vertice1
#print gon.vertice2

#line3 = poincare.genCircle(p1, p2)
#print line3.center
#print line3.radius
#p4 = poincare.getInverse(p3, line3)
#p4 = poincare.getMirrorPoint(p3, p1, p2)


def getGon(p, q, r, label):
#    print "getGon, label = {}".format(label)
    if label == "0" or label == "":
        return poincare.polygon(origin, verticeCount = 5, radius = r)
    else:
        iter = getGon(p, q, r, label[1:])
#        iter = copy.copy(iter)
#        print iter, iter.center
        return iter.getMirror(int(label[0]))


def getLabel(point):
    ret, iterPoint = getLabelIter(point)
    while iterPoint:
        iterRet, iterPoint = getLabelIter(iterPoint)
        ret = iterRet + ret
#        print ret
    return ret

def getLabelIter(point):
#    print "getLabelIter, z = {}".format(point.z)
#    pImg.drawPoint(point)
    for i in range(gon.verticeCount):
        p2 = gonFundamental.side(i + 1, point)
        if p2: 
#            p2 = poincare.getMirrorPoint(p1, gonFundamental.getVertice(i), gonFundamental.getVertice(i+1))
#        pImg.drawPoint(p2)
#        print "getLabelIter, p2.z = {}".format(p2.z)
#        if p2.r < point.r:
            return str(i + 1), p2
    return "", None
    
gon = getGon(5, 4, gonRadius, "0")
#pImg.drawPolygon(gon, color = (255, 0, 0))
#gon2 = getGon(5, 4, gonRadius, "1230")
#pImg.drawPolygon(gon2, color = (255, 0, 0))


colors = {
    "" : (255, 255, 255)
    ,"0" : (255, 255, 255)
    ,"1" : (255, 255, 0)
    ,"2" : (0, 255, 0)
    ,"3" : (0, 0, 255)
    ,"4" : (0, 255, 255)
    ,"5" : (255, 0, 255)
}


def colorFromLabel(label):
    hue = 0
    theta = (np.sqrt(5) + 1) / 2 % 1
    offset = theta
    for l in label:
        hue = hue + int(l) * offset
        offset = (offset + theta) % 1
    hue = int(hue % 1 * 180)
#    print hue
    return (hue, 255, 255)
        

for i in range(499):
    p1 = poincare.interiorPoint(np.exp(np.pi * 2j * random.random())* (1 - random.random() ** 3))
    label = getLabel(p1)
    p1.color = colorFromLabel(label)
    pImg.drawPoint(p1)
#    print p1, label
    gonTemp = getGon(5, 4, gonRadius, label)
    pImg.drawPolygon(gonTemp, color = (255, 0, 0))



#pImg.drawPolygon(getGon(5, 4, gonRadius, "1"), color = (0, 255, 0))

#for i in range(5):
#    print p1
#    p2 = gon.getVertice(i + 1)
#    pImg.drawPoint(p1)
#    c = poincare.genCircle(p1, p2)
#    pImg.drawCircle(c, color = (255, 255, 255))
#    gon2 = gon.getMirror(i)
#    pImg.drawPolygon(gon2)
#    pImg.drawPoint(gon2.center)
#    print gon2.vertices
#    for j in range(5):
#        p3 = gon2.getVertice(j)
#        print p3
#        pImg.drawPoint(p3)
        

#line1 = poincare.circle(somePoint = origin.z, someDirection = 1 * 1j, inverseRadius = 2.0)

#pImg.drawPoint(origin)
#pImg.drawPoint(p1)
#pImg.drawPoint(p2)
#pImg.drawPoint(p3)
#pImg.drawPoint(p4)

#line1 = p1.getPole()
#line2 = p2.getPole()

#pImg.drawCircle(line1, color = (255, 255, 255))
#pImg.drawCircle(line2, color = (255, 255, 255))

#pImg.drawCircle(line3, color = (255, 255, 255))

img = pImg.getImg()

img = cv2.cvtColor(img, cv2.COLOR_HSV2RGB)
cv2.imshow('myImg', img)
cv2.imwrite("lastPolygon.jpg", img)
cv2.waitKey(0)


