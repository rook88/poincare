import numpy as np
import cv2

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
        return point(f(self.z), self.color)
    def getMirror(self):
        return point(self.z * -1, self.color)
    def __str__(self):
        return str(self.z)
        
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
            self.direction = someDirection
        else:
            self.radius = 1 / self.inverseRadius
            self.center = self.somePoint + self.someDirection * 1j / self.inverseRadius
            self.direction = False
    def isLine(self):
        if self.inverseRadius < 1 / radiusOfLine:
            return True
        else:
            return False

class interiorPoint(point):
    pass

class exteriorPoint(point):
    pass

class poincareImg():
    def __init__(self 
                 ,size = [960, 960]
                 ,pointColor = (25, 25, 25)
                 ,pointRadius = 3
                 ,radius = 200
                 ):
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
        y = int(self.size[1] / 2 + self.radius * point.z.imag)
        if self.pointRadius > 0:
            cv2.circle(self.img, (x, y), self.pointRadius, point.color, -1)
        else:
            self.img[y, x] = point.color
    def drawCircle(self, circle):
        if circle.isLine():
            p1 = circle.somePoint * self.radius - radiusOfLine * circle.someDirection
            p2 = circle.somePoint * self.radius + radiusOfLine * circle.someDirection
            x1 = int(self.size[0] / 2 + p1.real)
            y1 = int(self.size[1] / 2 + p1.imag)
            x2 = int(self.size[0] / 2 + p2.real)
            y2 = int(self.size[1] / 2 + p2.imag)
            cv2.line(self.img, (x1, y1), (x2, y2), self.pointColor)
        else:
            center = circle.center
            x = int(self.size[0] / 2 + self.radius * center.real)
            y = int(self.size[1] / 2 + self.radius * center.imag)
            radius = int(circle.radius * self.radius)
            cv2.circle(self.img, (x, y), radius, self.pointColor, 1)
    def getImg(self):
        return self.img
                 
