import xml.etree.ElementTree as ET
from PIL import Image

import vector
import materials
import lights
import camera
import objects
import ray

import color


class Scene:
    ''' it's a room ... more or less
    '''
    def __init__(self, file_path):
        scene_xml = ET.parse(file_path)
        scene = scene_xml.getroot()
        self.materials = materials.parse(scene.find('materials'))
        self.objects = objects.parse(scene.find('objects'), self)
        self.lights = lights.parse(scene.find('lights'))
        self.background = color.parse(scene.find('background').find('color'))
        self.ambient_light = color.parse(scene.find('ambient').find('color'))
        self.camera = camera.Camera(scene.find('camera'))

    def send_ray(self, r, recursion_level=4):
    #does it make sense to set the recursion level per ray?
        ''' sends a ray t
            :param Ray r: starpoint and direction
            :pram int recursion_level: how many light recursion
        '''
        t_min = float('inf')
        for o in self.objects:
        #find the closest object
            t, tmp_point, tmp_normal = o.intersects(r)
            if t < t_min:
                t_min = t
                hit = o
                point = tmp_point
                normal = tmp_normal
                #normalvector

        if hit:
            new_color = hit.material.ambient_color * self.ambient_light
            #a tiny base glow of everything
            for ls in self.lights:
            #check all ligths
                if ls.is_visible_from_point(point, normal, self.objects):
                #if the light is visibile from the point the ray hit
                    if normal * ls.light_direction(point) > 0:
                    #if there is still light
                        sth = vector.dot(normal, ls.light_direction(point))
                        new_color += color.dot(hit.material.diffuse_color,
                                               ls.get_color(point) *
                                               sth)

                        lr = -(2 * vector.dot(normal,
                                              ls.light_direction(point) *
                                              normal -
                                              ls.light_direction(point)))

                        new_color += (hit.material.specular_color *
                                      ls.get_color(point) *
                                      lr *
                                      r.direction /
                                      (lr.length * r.direction.length) **
                                      hit.material.phong_specular_exponent)

            if recursion_level < 0:
                return new_color

            r2 = ray.Ray(point + 0.01 * normal, -(2 * (normal * r.direction) *
                                                  normal - r.direction))
            new_color += color.dot(hit.material.reflection_color,
                                   self.rend_ray(r2, recursion_level - 1))
            return new_color
        else:
            return self.background

    def render(self, v_res):
        h_res = int(camera.aspect_ratio * v_res)
        outfile = Image.new('RGB', h_res, v_res)

        for x in range(0, h_res):
            for y in range(0, v_res):
                pixel = (self.camera.virtual_screen_top_left_corner +
                         x /
                         float(h_res) *
                         -self.camera.view_left *
                         self.camera.virtual_screen_width)
                direction = pixel - self.camera.position
                outfile[x, y] = self.send_ray(ray.Ray(pixel,
                                                      direction)).get_color()
        return outfile

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
