import math
import vector


class Camera:
    def __init__(self, cam_node):
        '''
            raises: if position, target or up vector is not set in XML file
        '''
        self._near_clipping = 1.0
        self._viewing_angle = 22.5
        self._aspect_ratio = 1.0
        for node in cam_node:
            if node.tag == 'position':
                self._position = vector.Vector3D(float(node[0].get('x')),
                                                 float(node[0].get('y')),
                                                 float(node[0].get('z')))
            elif node.tag == 'lookat':
                self._target = vector.Vector3D(float(node[0].get('x')),
                                               float(node[0].get('y')),
                                               float(node[0].get('z')))
            elif node.tag == 'upvector':
                self._up_vector = vector.Vector3D(float(node[0].get('x')),
                                                  float(node[0].get('y')),
                                                  float(node[0].get('z')))
            elif node.tag == 'options':
                self._near_clipping = float(node.get('nearclipping'))
                self._viewing_angle = float(node.get('fov'))
                self._aspect_ratio = float(node.get('aspectratio'))
        if self._position is None:
            raise Exception("Error in Camera(): No position defined")
        if self._target is None:
            raise Exception("Error in Camera(): No target defined")
        if self._up_vector is None:
            raise Exception("Error in Camera(): No up vector defined")

    @property
    def viewing_direction(self):
        return (self._target - self._position).normalized

    @property
    def up_vector(self):
        return self._up_vector

    @property
    def view_up(self):
        return (self.viewing_direction ^ self.view_left).normalized

    @property
    def view_left(self):
        return (self._up_vector ^ self.viewing_direction).normalized

    @property
    def angle(self):
        return self._viewing_angle

    @property
    def near_clipping(self):
        return self._near_clipping

    @property
    def position(self):
        return self._position

    @property
    def virtual_screen_height(self):
        return (2 * math.tan(self._viewing_angle / 360 * math.PI) *
                self._near_clipping)

    @property
    def virtual_screen_width(self):
        return self._aspect_ratio * self.virtual_screen_height

    @property
    def virtual_screen_top_left_corner(self):
        mittelpunkt = (self._position + self._near_clipping +
                       self.viewing_direction)
        return (mittelpunkt +
                self.virtual_screen_height / 2 * self.view_up.normalized +
                self.virtual_screen_width / 2 * self.view_left.normalized)

    @property
    def aspect_ratio(self):
        return self._aspect_ratio
