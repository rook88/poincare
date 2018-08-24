import numpy as np
import cv2
import getopt, sys

testMode = False
imagePath = ""
outputFile = ""
depth = 4
p = 3
q = 7
frameCount = 1
zoom = 1.0
multiplier = 0.0

opts, args = getopt.getopt(sys.argv[1:], None, [
    'test'
    ,'imagepath='
    ,'file='
    ,'depth='
    ,'p='
    ,'q='
    ,'frames='
    ,'zoom='
    ,'multiplier='
])

cWhite = (255, 255, 0)

for o, a in opts:
    if o == '--test':
        testMode = True
    if o == '--imagepath':
        imagePath = a
    if o == '--file':
        outputFile = a
    if o == '--depth':
        depth = int(a)
    if o == '--p':
        p = int(a)
    if o == '--q':
        q = int(a)
    if o == '--frames':
        frameCount = int(a)
    if o == '--zoom':
        zoom = float(a)
    if o == '--multiplier':
        multiplier = float(a)
        

def zoomPoint(z):
    return zoom * z
    

radiusOfLine = 10000.0

def z2xy(z):
    return (np.real(z), np.imag(z))

def intersection(l1, l2):
    (x1, y1) = z2xy(l1.somePoint)
    (x2, y2) = z2xy(l1.somePoint + l1.direction)
    (x3, y3) = z2xy(l2.somePoint)
    (x4, y4) = z2xy(l2.somePoint + l2.direction)
    if ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) == 0:
        return None
    else:
        ret = ((x1*y2 - y1*x2) * (x3 - x4) - (x1 - x2) * (x3*y4 - y3*x4)) / ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) + ((x1*y2 - y1*x2) * (y3 - y4) - (y1 - y2) * (x3*y4 - y3*x4)) / ((x1- x2)*(y3- y4) - (y1 - y2)*(x3 - x4)) * 1j
        if np.abs(ret) > radiusOfLine:
            return None
        else:
            return point(ret)

class point():
    def __init__(self, z, color = np.array([255, 255, 255])):
        self.z = z
        self.r = abs(z)
        self.color = color
#      self.color = self.color * (1 - self.r) ** 0.2
        self.key = z
    def getInverse(self):
        ret = self.z / self.r ** 2
        return exteriorPoint(ret)
    def map(self, f):
        self.z = f(self.z)
    def getCopy(self):
        return point(self.z, self.color)
    def getMapped(self, f):
        return interiorPoint(f(self.z), self.color)
    def getMirror(self):
        return point(self.z * -1, self.color)
    def __str__(self):
        return "point " + str(self.z)

class interiorPoint(point):
    def getPole(self):
        pInv = self.getInverse()
        b = exteriorPoint(0.5 * (self.z + pInv.z))
        ret = circle(somePoint = b.z, someDirection = b.z * 1j, inverseRadius = 0.0) 
        return ret

origin = interiorPoint(0.0000 + 0.000j)

class exteriorPoint(point):
    pass

        
class isometry():
    def __init__(self, fromPoint, toPoint):
        def map(z):
            ret = (z + toPoint.z) / (1 + z * toPoint.z.conjugate())
            return ret
        self.map = map

class circle():
    def __init__(self, somePoint = 1.0 + 0.0j, someDirection = 0.0 + 1.0j, inverseRadius = 1.0, center = None, radius = None):
        if center == None:
            self.somePoint = somePoint
            self.someDirection = someDirection
            self.inverseRadius = inverseRadius
        else:
            self.somePoint = center + radius
            self.someDirection = 1j
            self.inverseRadius = 1 / radius
        if self.isLine():
            self.radius = None
            self.center = None
            self.direction = someDirection / abs(someDirection)
        else:
            self.radius = 1 / self.inverseRadius
            self.center = self.somePoint + self.someDirection * 1j / self.inverseRadius
            self.direction = None
    def __str__(self):
        ret = "circle, center = {center}, some point = {somePoint}, some direction = {someDirection}".format(**self.__dict__)
        return ret
    def __eq__(self, other):
        if self.isLine():
            if other.isLine():
                return self.direction == other.direction
            else:
                return False
        else:
            if other.isLine():
                return False
            else:
                return self.radius == other.radius and self.center == other.center
        
    def isLine(self):
        if self.inverseRadius < 1 / radiusOfLine:
            return True
        else:
            return False
    def getSomePoints(self):
        if self.isLine():
            p1 = self.somePoint
            p2 = self.somePoint + self.someDirection
            p3 = self.somePoint - self.someDirection
        else:
            p1 = self.center + self.radius
            p2 = self.center + self.radius * 1j
            p3 = self.center - self.radius * 1j
        return (p1, p2, p3)
    def getKey(self):
        return str(np.round(self.center.real, 5)) + "," + str(np.round(self.center.imag, 5)) 


def genCircle(somePoint, someOtherPoint):
    l1 = somePoint.getPole()
    l2 = someOtherPoint.getPole()
    b = intersection(l1, l2)
#    print somePoint, someOtherPoint, b
    if b == None:
        b = exteriorPoint((somePoint.z - someOtherPoint.z) * 1j * 10000.0)
    ret = circle(center = b.z, radius = abs(b.z - somePoint.z))
    return ret

def genCircleFromPoints(p1, p2, p3):
#    print "gen circle from points: ", p1, p2, p3
    l1 = circle(somePoint = (p1 + p2) / 2, someDirection = (p2 - p1) * 1j, inverseRadius = 0.0)
    l2 = circle(somePoint = (p1 + p3) / 2, someDirection = (p3 - p1) * 1j, inverseRadius = 0.0)
    center = intersection(l1, l2)
    if center:
        radius = abs(p1 - center.z)
        ret = circle(center = center.z, radius = radius)
#        print center, radius, ret
    else:
        ret = l1
    return ret

def getInverse(point, circle):
    if circle.isLine():
        return np.conjugate((point - circle.somePoint) / circle.direction) * circle.direction + circle.somePoint
    else:
        return np.conjugate(circle.radius ** 2 /(point - circle.center)) + circle.center

def getInverseCircle(circle_1, circle_2):
    p1, p2, p3 = circle_1.getSomePoints()
    q1 = getInverse(p1, circle_2)
    q2 = getInverse(p2, circle_2)
    q3 = getInverse(p3, circle_2)
#    print q1, q2, q3
    return genCircleFromPoints(q1, q2, q3)
#    print p1, p2, p3


def getMirrorPoint(p1, p2, p3):
    return getInverse(p1, genCircle(p2, p3))

class segment():
    def __init__(self, p1, p2):
        self.p1 = p1
        self.p2 = p2

class polygon():
    def __init__(self, center, vertice1 = origin, vertice2 = origin, verticeCount = 0, radius = 0, vertices = []):
        self.center = center
        if verticeCount and radius:
            self.vertices = []
            for i in range(verticeCount):
                self.vertices.append(interiorPoint(radius * np.exp(2j * i * np.pi / verticeCount)))
        else:
            self.vertices = vertices
        self.verticeCount = len(self.vertices)
        self.radius = radius
    def __str__(self):
        return "{:.5} + {:.5}j".format(np.real(self.center.z), np.imag(self.center.z))
    def getVerticeZoomed(self, n):
        retN = self.vertices[n % self.verticeCount].getMapped(zoomPoint)
        return retN
    def getVertice(self, n):
        ret = self.vertices[n % self.verticeCount]
        return ret
    def getMirror(self, n):
        p1 = self.getVertice(n - 1)
        p2 = self.getVertice(n)
        retCenter = getMirrorPoint(self.center, p1, p2)
        retVertices = []
        for v in self.vertices:
            retv = getMirrorPoint(v, p1, p2)
#            print v, retv
            retVertices.append(retv)
        ret = polygon(retCenter, vertices = retVertices)
        return ret
    def side(self, n, point):
        p1 = self.getVertice(n - 1)
        p2 = self.getVertice(n)
        c = genCircle(p1, p2)
        p = getMirrorPoint(point, p1, p2)
#        print point, c.center, p, abs(point.z - c.center), abs(p.z - c.center)
        if abs(point.z - c.center) <= abs(p.z - c.center):
            return p
        else:
            return None


    def getEdges(self):
        ret = []
        for i in range(self.verticeCount):
            ret.append(segment)

class poincareImg():
    def __init__(self 
                 ,size = [960, 960]
                 ,pointColor = (25, 25, 25)
                 ,pointRadius = 3
                 ,radius = 200
                 ,backgroundIsWhite = False):
        self.img = np.zeros((size[1], size[0], 3), dtype=np.uint8)
        self.size = size
        self.pointRadius = pointRadius
        self.pointColor = pointColor
        self.radius = radius
    def drawEdge(self):
        x = int(self.size[0] / 2)
        y = int(self.size[1] / 2)
        cv2.circle(self.img, (x, y), self.radius, self.pointColor, 2)
    def drawPoint(self, point):
        x = int(self.size[0] / 2 + self.radius * point.z.real)
        y = int(self.size[1] / 2 - self.radius * point.z.imag)
        if self.pointRadius > 0:
            cv2.circle(self.img, (x, y), self.pointRadius, point.color, -1)
        else:
            self.img[y, x] = point.color
    def drawCircle(self, circle, color = cWhite, fill = False, thickness = 1):
        if circle.isLine():
            p1 = circle.somePoint * self.radius - radiusOfLine * circle.someDirection
            p2 = circle.somePoint * self.radius + radiusOfLine * circle.someDirection
            x1 = int(self.size[0] / 2 + p1.real)
            y1 = int(self.size[1] / 2 - p1.imag)
            x2 = int(self.size[0] / 2 + p2.real)
            y2 = int(self.size[1] / 2 - p2.imag)
            cv2.line(self.img, (x1, y1), (x2, y2), color)
        else:
            center = circle.center
            x = int(self.size[0] / 2 + self.radius * center.real)
            y = int(self.size[1] / 2 - self.radius * center.imag)
            radius = int(circle.radius * self.radius)
            if fill:
                thickness = -1
#            else:
#                thickness = 1
            cv2.circle(self.img, (x, y), radius, color, thickness)
    def getImg(self, multiplier = 1.0, hasMask = True, resize = None):
        mask = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        x = int(self.size[0] / 2)
        y = int(self.size[1] / 2)
        cv2.circle(mask, (x, y), int(self.radius * multiplier), (255, 255, 255), -1)
        if hasMask:
            ret = cv2.bitwise_and(self.img, mask) 
        else:
            ret = self.img
        if resize:
            ret = cv2.blur(ret, (3, 3))
            ret = cv2.resize(ret, dsize = resize)
        return ret
    def drawPolygon(self, pg, color = (0, 0, 255), offset = 1.0):
        mask = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        maskComplement = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        maskIter = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        maskIterComplement = np.zeros((self.size[1], self.size[0], 3), dtype=np.uint8)
        mask[:] = color
#        maskComplement[:] = (255, 255, 255)
        pc = pg.center
        for i in range(pg.verticeCount):
            p1 = pg.getVertice(i)
            p2 = pg.getVertice(i + 1)
            c = genCircle(p1, p2)
            center = c.center
            x = int(self.size[0] / 2 + self.radius * offset * center.real)
            y = int(self.size[1] / 2 - self.radius * offset * center.imag)
            radius = int(c.radius * self.radius * offset) 
            if abs(pc.z - center) > abs(p1.z - center):
                maskIter[:] = color
                maskIterComplement[:] = (0, 0, 0)
                cv2.circle(maskIter, (x, y), radius + 3, (0, 0, 0), -1)
                cv2.circle(maskIterComplement, (x, y), radius - 3, (255, 255, 255), -1)
            else:
                maskIter[:] = (0, 0, 0)
                maskIterComplement[:] = (255, 255, 255)
                cv2.circle(maskIter, (x, y), radius - 3, color, -1)
                cv2.circle(maskIterComplement, (x, y), radius + 3, (0, 0, 0), -1)
            mask = cv2.bitwise_and(maskIter, mask)
            maskComplement = cv2.bitwise_or(maskIterComplement, maskComplement)
#            cv2.circle(self.img, (x, y), radius, (0, 0, 255), 1)
        self.img = cv2.bitwise_and(self.img, maskComplement)
        self.img = cv2.bitwise_or(self.img, mask)
"""
        print color
        cv2.imshow('self.img', cv2.cvtColor(self.img, cv2.COLOR_HSV2RGB))
        cv2.waitKey(0)
        cv2.destroyAllWindows()
            
           cv2.imshow('mask', mask)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
            cv2.imshow('maskComplement', maskComplement)
            cv2.waitKey(0)
            cv2.destroyAllWindows()
"""
            
            



