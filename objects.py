import vector
import math


def parse(obj_node):
    objects = []
    for obj in obj_node:
        if obj.tag == 'sphere':
            objects.add(RaytracerSphere(obj))


class RaytracerObject:
    def __init__(self, node, scene):
        self.name = node.attrib('name')
        self.material = scene.get_material_by_name(node.attrib['material'])


class RaytracerSphere(RaytracerObject):
    def __init__(self, node, scene):
        super(RaytracerSphere, self).__init__(node, scene)
        self._radius = float(node.attrib['radius'])
        self._center = vector.parse(node[0])

    def intersects(self, r):
        y = r.start - self._center
        c = vector.dot(y, y) - self._radius * self._radius
        b = vector.dot(r.direction, y)
        if b*b - c < 0:
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
