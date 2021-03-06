import math


def dot(a, b):
    return a.x*b.x + a.y*b.y + a.z*b.z


def cross(a, b):
    return Vector3D(a.y*b.z-a.z*b.y,
                    a.z*b.x-a.x*b.z,
                    a.x*b.y-a.y*b.x)


class Vector3D:
    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    @property
    def normalized(self):
        return self * (1.0 / self.length)

    @property
    def length(self):
        return math.sqrt(self.x * self.x +
                         self.y * self.y +
                         self.z * self.z)

    #def __div__(self, a):
    #    return Vector3D(self.x/a, self.y/a, self.z/a)

    def __mul__(self, a):
        return Vector3D(self.x*a, self.y*a, self.z*a)

    def __rmul__(self, a):
        return self * a

    def __str__(self):
        return "Vector3D(%g,%g,%g)" % (self.x, self.y, self.z)

    def __add__(self, a):
        return Vector3D(self.x + a.x,
                        self.y + a.y,
                        self.z + a.z)

    def __neg__(self):
        return Vector3D(-self.x,
                        -self.y,
                        -self.z)

    def __sub__(self, a):
        return self + (-a)
