import ray
import math
import vector
import color


class LightSource:

    def get_color(self, p):
        '''
            :param Vector3D p: ??
        '''
        return self._color

    @property
    def name(self):
        return self._name

    def light_direction(self, p):
        ''' from p to the light source
            :param Vector3D p: ??
        '''
        pass

    def is_visibible_from_point(self, point, normal, objects):
        '''
            :parame Vector3D point:
            :param Vector3D normal:
            :param objects:
            :rtype: bool
        '''
        pass


class FalloffLightSource(LightSource):
    def __init__(self, name, factor, position, color):
        self._name = name
        self._factor = factor
        self._position = position
        self._color = color

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position +
                ", color = " + self._color)

    def is_visible_from_point(self, point, normal, objects):
        for o in objects:
            tmp, tmp_point, tmp_nomal = o.intersects(ray.Ray(point +
                                                             0.01 * normal,
                                                             self._position -
                                                             point,
                                                             (point -
                                                              self._position)
                                                             .length))
            if tmp < float('inf'):
                return False
        return True

    def get_color(self, p):
        '''
            :param Vector3D p: ??
        '''
        return (self._color * self._factor *
               (1.0 / (p - self._position).length ** 2)).sanitized

    def light_direction(self, p):
        ''' from p to the light source
            :param Vector3D p: ??
        '''
        return (self._position - p).normalized


class SpotLightSource(LightSource):
    def __init__(self, name, angle, position, target, color):
        self._name = name
        self._angle = angle / 360 * math.pi
        self._position = position
        self._direction = (target - position).normalized
        self._color = color

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position +
                ", color = " + self._color)

    def is_visible_from_point(self, point, normal, objects):
        for o in objects:
            tmp, tmp_point, tmp_nomal = o.intersects(ray.Ray(point +
                                                             0.01 * normal,
                                                             self._position -
                                                             point,
                                                             (point -
                                                              self._position)
                                                             .length))
            if tmp < float('inf'):
                return False
        return True

    def get_color(self, p):
        '''
            :param Vector3D p: ??
        '''
        if self._angle < math.acos(vector.dot(self._direction,
                                              p - self._position) /
                                  (p - self._position).length):
            return color.RaytracerColor()
        return self._color

    def light_direction(self, p):
        ''' from p to the light source
            :param Vector3D p: ??
        '''
        return (self._position - p).normalized


class ParallelLightSource(LightSource):
    def __init__(self, name, direction, color):
        self._name = name
        self._direction = direction
        self._color = color

    def __str__(self):
        return ("ParallelLightSource: name = '" + self._name +
                "', direction = " + self._direction +
                ", color = " + self._color)

    def light_direction(self, p):
        ''' from p to the light source
            :param Vector3D p: ??
        '''
        return -self._direction.normalized

    def is_visible_from_point(self, point, normal, objects):
        for o in objects:
            tmp, tmp_point, tmp_normal = o.intersects(ray.Ray(point +
                                                              0.01 * normal,
                                                      -self._direction))
            if tmp < float('inf'):
                return False
        return True


class OmniLightSource(LightSource):
    def __init__(self, name, position, color):
        self._name = name
        self._position = position
        self._color = color

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position +
                ", color = " + self._color)

    def is_visible_from_point(self, point, normal, objects):
        for o in objects:
            tmp, tmp_point, tmp_nomal = o.intersects(ray.Ray(point +
                                                             0.01 * normal,
                                                             self._position -
                                                             point,
                                                             (point -
                                                              self._position)
                                                             .length))
            if tmp < float('inf'):
                return False
        return True

    def light_direction(self, p):
        ''' from p to the light source
            :param Vector3D p: ??
        '''
        return (self._position - p).normalized
