def dot(a, b):
    ''' Matrixmultiplication
        :param RaytracerColor a: color triple
        :param RaytracerColor b: color triple
        :returns matrixmultiplicition of a and b
    '''
    return RaytracerColor(a.r * b.r, a.g * b.g, a.b * b.b)

def parse(color_node):
    return RaytracerColor(color_node.attrib['r'],
                          color_node.attrib['g'],
                          color_node.attrib['b'])


class RaytracerColor:
    ''' represents a color
    '''
    def __init__(self, r=0.0, g=0.0, b=0.0):
        ''' :param float r: red color component between 0 and 1
            :param float g: green color component between 0 and 1
            :param float b: blue color component between 0 and 1
            :var float r: red color component between 0 and 1
            :var float g: green color component between 0 and 1
            :var float b: blue color component between 0 and 1
        '''
        self._r = r
        self._g = g
        self._b = b

    @property
    def r(self):
        return self._r

    @property
    def g(self):
        return self._g

    @property
    def b(self):
        return self._b

    def __add__(self, a):
        ''' Matrixaddition
            :param RaytracerColor a: color triple
            :param RaytracerColor b: color triple
            :returns matrxaddition of a and b
        '''
        return RaytracerColor(self.r + a.r, self.g + a.g, self.b + a.b)

    def __mul__(self, a):
        ''' Scalarmultiplication
            :param float a: scalar
            :param RaytracerColor b: color triple
            :returns scalarmultiplicition of a and b
        '''
        return RaytracerColor(self.r * a, self.g * a, self.b * a)
