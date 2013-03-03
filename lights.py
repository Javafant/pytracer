import color
import ray


def parse(lights_node):
    lights = []
    for node in lights_node:
        lights.append(create_light_source(node))


def create_light_source(light_node):
    ''' creates a light source of the type
        omnilight, parallellight, spotlight or falllight
        :param light_node: a XML node that represents the light source
        :raises: if name of light_node is not a known light type
    '''
    if light_node.tag == 'omnilight':
        return OmniLightSource(light_node)
    elif light_node.tag == 'parallellight':
        return ParallelLightSource(light_node)
    elif light_node.tag == 'spotlight':
        return SpotLightSource(light_node)
    elif light_node.tag == 'falllight':
        return FalloffLightSource(light_node)
    raise Exception("Error in create_light_source(): Unknown light type '" +
                    light_node.tag + "'")


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
    def __init__(self, light_node):
        if light_node.get('name') is None:
            raise Exception('Error in OmniLightSource(): no name define')
        self._name = light_node.get('name')
        if light_node.find('vector3d') is None:
            raise Exception('Error in OmniLightSource(): no position defined')
        self._position = color.Color(light_node.find('vector3d'))
        if light_node.find('color') is None:
            raise Exception('Error in OmniLightSource(): no color defined')
        self._color = color.Color(light_node.find('color'))

    def __str__(self):
        return ("FalloffLightSource: name = '" + self._name +
                "', position = " + self._position +
                ", color = " + self._color)

    def is_visibible_from_point(self, point, normal, objects):
        for o in objects:
            tmp, tmp_point, tmp_nomal = o.intersects(ray.Ray(point + 0.01 * normal,
                                                             self._position - point,
                                                             (point - self._position).length))
            if tmp < float('inf'):
                return False
        return True
