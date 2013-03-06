import vector
import math


class RaytracerObject(object):
    def __init__(self, name, material):
        self.name = name
        self.material = material


class RaytracerSphere(RaytracerObject):
    def __init__(self, name, material, radius, center):
        super(RaytracerSphere, self).__init__(name, material)
        self._radius = radius
        self._center = center

    def intersects(self, r):
        ''' ???
            :param Ray r:
            :returns: ?, point, normal
            :rtype: float, Vector3D, Vector3D
        '''
        y = r.start - self._center
        c = vector.dot(y, y) - self._radius * self._radius
        b = vector.dot(r.direction, y)
        if b * b - c < 0:
            return float('inf'), None, None
        t1 = -b + math.sqrt(b * b - c)
        t2 = -b - math.sqrt(b * b - c)

        if t1 < 0:
            return float('inf'), None, None
        else:
            if t2 < 0:
                point = r.start + r.direction * t1
                normal = (point - self._center).normalized
                if t1 < r.t_max:
                    return t1, point, normal
                else:
                    return float('inf'), None, None
            else:
                point = r.start + r.direction * t2
                normal = (point - self._center).normalized
                if t2 < r.t_max:
                    return t2, point, normal
                else:
                    return float('inf'), None, None
