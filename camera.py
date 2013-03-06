import math
import vector


class Camera:
    def __init__(self, position, target, up_vector,
                 near_clipping, viewing_angle, aspect_ratio):
        '''
        Initializes the camera parameters
        '''

        self._position = position
        self._target = target
        self._up_vector = up_vector
        self._near_clipping = near_clipping
        self._viewing_angle = viewing_angle
        self._aspect_ratio = aspect_ratio

    @property
    def viewing_direction(self):
        return (self._target - self._position).normalized

    @property
    def up_vector(self):
        return self._up_vector

    @property
    def view_up(self):
        return (vector.cross(self.viewing_direction,
                             self.view_left)).normalized

    @property
    def view_left(self):
        return (vector.cross(self._up_vector,
                             self.viewing_direction)).normalized

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
        return (2 * math.tan(self._viewing_angle / 360.0 * math.pi) *
                self._near_clipping)

    @property
    def virtual_screen_width(self):
        return self._aspect_ratio * self.virtual_screen_height

    @property
    def virtual_screen_top_left_corner(self):
        mittelpunkt = (self._position + self.viewing_direction *
                       self.near_clipping)
        return (mittelpunkt +
                self.virtual_screen_height / 2.0 * self.view_up.normalized +
                self.virtual_screen_width / 2.0 * self.view_left.normalized)

    @property
    def aspect_ratio(self):
        return self._aspect_ratio
