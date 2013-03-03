import vector


class Ray:
    def __init__(self, start, direction, t_max=float('inf')):
        '''
            :param Vector3D start: a vector representing the start point
            :param Vector3D direction: a vectior representing the direction of the ray
            :param float t_max: the maximal length of the ray ?? default: positive infinity
        '''
        self._start = start
        self._direction = direction.normalized
        self._t_max = t_max

    @property
    def start(self):
        return self._start

    @property
    def dirction(self):
        return self._direction

    @property
    def t_max(self):
        return self._t_max

