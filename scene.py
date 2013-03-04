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
        #we forgot the defaul background
        self.ambient_light = color.parse(scene.find('ambient').find('color'))
        self.camera = camera.Camera(scene.find('camera'))

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
        stacking_reflection = white
        while i < recursion_level and (i == 0 or ((last_hit is not None) and (stacking_reflection <> black)):
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
                new_color = color.dot(hit.material.ambient_color, self.ambient_light)
                #a tiny base glow of everything
                for ls in self.lights:
                #check all ligths
                    if ls.is_visible_from_point(point, normal, self.objects):
                    #if the light is visibile from the point the ray hit
                        light_direction = vector.dot(normal, ls.light_direction(point))
                        if light_direction > 0:
                        #if there is still light
                            new_color += (color.dot(hit.material.diffuse_color,
                                                   ls.get_color(point)) *
                                                   light_direction)

                            lr = -(2 * vector.dot(normal,
                                                  ls.light_direction(point)) *
                                                  normal -
                                                  ls.light_direction(point))

                            new_color += (color.dot(hit.material.specular_color,
                                                    ls.get_color(point)) *
                                                    (vector.dot(lr, myray.direction) /
                                                     (lr.length * myray.direction.length)) **
                                          hit.material.phong_specular_exponent)
                #get the next ray
                myray = ray.Ray(point + 0.01 * normal, -(2 * (vector.dot(normal, myray.direction)) *
                                                      normal - myray.direction))
            if last_hit is not None:
                #respect the reflectioncolor of the last element
                #ret_color += color.dot(last_hit.material.reflection_color,
                #                       new_color)
                stacking_reflection = color.dot(last_hit.material.reflection_color, stacking_reflection)
            #else:
            #    ret_color = new_color

            ret_color += color.dot(stacking_reflection,
                                       new_color)
            last_hit = hit
            i += 1
        return ret_color

    def render(self, v_res):
        h_res = int(self.camera.aspect_ratio * v_res)
        outfile = Image.new('RGB', (h_res, v_res))
        pix = outfile.load()
        pixbuffer = []

        for x in range(0, h_res):
            for y in range(0, v_res):
                pixel = (self.camera.virtual_screen_top_left_corner +
                         float(x) /
                         float(h_res) *
                         -self.camera.view_left *
                         self.camera.virtual_screen_width +
                         float(y) /
                         float(v_res) *
                         -self.camera.view_up *
                         self.camera.virtual_screen_height)
                direction = pixel - self.camera.position
                #pixbuffer.append(self.send_ray(ray.Ray(pixel,
                #                                  direction)).get_color())
                pix[x, y] = self.send_ray(ray.Ray(pixel,
                                                  direction)).get_color()
                #pix((x, y), self.send_ray(ray.Ray(pixel,
                #                                  direction)).get_color())
        outfile.putdata(pixbuffer)
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
