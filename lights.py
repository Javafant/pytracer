import ray


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
        return (self._position - p).normalized

    def is_visibible_from_point(self, point, normal, objects):
        '''
            :parame Vector3D point:
            :param Vector3D normal:
            :param objects:
            :rtype: bool
        '''
        pass


class FalloffLightSource(LightSource):
    def __init__(self):
        pass

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position + ", color = " +
                self._color + ", factor = " + self._factor)


class SpotLightSource(LightSource):
    def __init__(self):
        pass

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position + ", target = " +
                self._target + ", color = " + self._color +
                ", angle = " + self._angle)


class ParallelLightSource(LightSource):
    def __init__(self):
        pass

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position +
                ", color = " + self._color)


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
