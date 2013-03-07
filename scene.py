import vector
import ray

import color

import sys


class Scene:
    ''' it's a room ... more or less
    '''
    def __init__(self, camera, objects, materials,
                 lights, background, ambient_light):
        self.camera = camera
        self.objects = objects
        self.materials = materials
        self.lights = lights
        self.background = background
        self.ambient_light = ambient_light

    def send_ray(self, r, recursion_level=4):
    #does it make sense to set the recursion level per ray?
        ''' sends a ray t
            :param Ray r: starpoint and direction
            :pram int recursion_level: how many light recursion
        '''
        i = 0
        myray = r
        last_hit = None
        #we don't need to check the the last object, we are comming from
        black = color.RaytracerColor(0.0, 0.0, 0.0)
        white = color.RaytracerColor(1.0, 1.0, 1.0)
        ret_color = self.background
        reflexion_stack = white
        while i < recursion_level and (i == 0 or
                                       ((last_hit is not None) and
                                        (reflexion_stack != black))):
            t_min = float('inf')
            hit = None
            new_color = self.background
            for o in self.objects:
            #find the closest object
                if o != last_hit:
                    t, tmp_point, tmp_normal = o.intersects(myray)
                    if t < t_min:
                        t_min = t
                        hit = o
                        point = tmp_point
                        normal = tmp_normal
                        #normalvector

            if hit is not None:
                new_color = color.dot(hit.material.ambient_color,
                                      self.ambient_light)
                #a tiny base glow of everything
                for ls in self.lights:
                #check all ligths
                    if ls.is_visible_from_point(point, normal, self.objects):
                    #if the light is visibile from the point the ray hit
                        light_direction = ls.light_direction(point)
                        light_scalar = vector.dot(normal,
                                                  light_direction)
                        if light_scalar > 0:
                        #if there is still light
                            #hm and md for line shortening
                            hm = hit.material
                            md = myray.direction
                            new_color += (color.dot(hm.diffuse_color,
                                                    ls.get_color(point)) *
                                          light_scalar)

                            lr = -(2 * vector.dot(normal,
                                                  light_direction) *
                                   normal -
                                   light_direction)

                            new_color += (color.dot(hm.specular_color,
                                                    ls.get_color(point)) *
                                          (vector.dot(lr, md) /
                                           (lr.length * md.length)) **
                                          hm.phong_specular_exponent)
                #get the next ray
                myray = ray.Ray(point + 0.01 * normal,
                                -(2 * (vector.dot(normal, myray.direction)) *
                                  normal - myray.direction))
            if last_hit is not None:
                reflexion_stack = color.dot(last_hit.material.reflection_color,
                                            reflexion_stack)

            ret_color += color.dot(reflexion_stack,
                                   new_color)
            last_hit = hit
            i += 1
        return ret_color

    def render(self, v_res):
        print('rendering started')
        h_res = int(round(self.camera.aspect_ratio * v_res))
        pixbuffer = []
        wstep = (1.0 / float(h_res) *
                 -self.camera.view_left * self.camera.virtual_screen_width)
        hstep = (1.0 / float(v_res) *
                 -self.camera.view_up * self.camera.virtual_screen_height)

        for y in range(0, v_res):
            sys.stdout.write('\r' + str(y*100/v_res) + '% rendered')
            sys.stdout.flush()
            pixel = (self.camera.virtual_screen_top_left_corner + y * hstep)
            for x in range(0, h_res):
                pixel += wstep
                direction = pixel - self.camera.position
                pixbuffer.append(self.send_ray(ray.Ray(pixel,
                                                       direction)).get_color())
        print('\nrendering completed')
        return pixbuffer

    def get_material_by_name(self, strName):
        '''
            :param str strName: name of the wanted material
            :returns: a material with strName as name or non if not found
            :rtype: Material  or None if not found
        '''
        for m in self.materials:
            if m.name == strName:
                return m
        return None
