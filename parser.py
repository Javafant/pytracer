import xml.etree.ElementTree as ET
from scene import Scene
from camera import Camera
from materials import Material, get_material_by_name
from objects import RaytracerSphere
from color import RaytracerColor
from lights import (OmniLightSource, ParallelLightSource,
                    SpotLightSource, FalloffLightSource)
from vector import Vector3D


class Parser:
    def __init__(self, file_path):
        self.scene_xml = ET.parse(file_path)

    def parse(self):
        scene = self.scene_xml.getroot()
        camera = self._parse_camera(scene.find('camera'))
        materials = self._parse_materials(scene.find('materials'))
        objects = self._parse_objects(scene.find('objects'), materials)
        lights = self._parse_lights(scene.find('lights'))
        background = self._parse_color(scene.find('background').find('color'))
        ambient_light = self._parse_color(scene.find('ambient').find('color'))

        return Scene(camera, objects, materials,
                     lights, background, ambient_light)

    def _parse_camera(self, camera_node):
        '''
            raises: if position, target or up vector is not set in XML file
        '''
        near_clipping = 1.0
        viewing_angle = 22.5
        aspect_ratio = 1.0
        for node in camera_node:
            if node.tag == 'position':
                position = self._parse_vector(node[0])
            elif node.tag == 'lookat':
                target = self._parse_vector(node[0])
            elif node.tag == 'upvector':
                up_vector = self._parse_vector(node[0])
            elif node.tag == 'options':
                near_clipping = float(node.get('nearclipping'))
                viewing_angle = float(node.get('fov'))
                aspect_ratio = float(node.get('aspectratio'))
        if position is None:
            raise Exception("Error in Camera(): No position defined")
        if target is None:
            raise Exception("Error in Camera(): No target defined")
        if up_vector is None:
            raise Exception("Error in Camera(): No up vector defined")

        return Camera(position, target, up_vector,
                      near_clipping, viewing_angle, aspect_ratio)

    def _parse_objects(self, objects_node, materials):
        objects = []
        for object_node in objects_node:
            if object_node.tag == 'sphere':
                objects.append(self._parse_raytracer_sphere(object_node,
                                                            materials))
        return objects

    def _parse_raytracer_sphere(self, object_node, materials):
        name = object_node.get('name')
        material = get_material_by_name(object_node.get('material'), materials)
        radius = float(object_node.get('radius'))
        center = self._parse_vector(object_node[0])
        return RaytracerSphere(name, material, radius, center)

    def _parse_materials(self, materials_node):
        materials = []
        for material_node in materials_node:
            materials.append(self._parse_material(material_node))
        return materials

    def _parse_material(self, material_node):
        name = material_node.get('name')
        for color in material_node:
            if color.tag == 'ambient':
                ambient_color = self._parse_color(color[0])
                ambient_color *= float(color.get('factor'))
            elif color.tag == 'diffuse':
                diffuse_color = self._parse_color(color[0])
                diffuse_color *= float(color.get('factor'))
            elif color.tag == 'specular':
                specular_color = self._parse_color(color[0])
                specular_color *= float(color.get('factor'))
                phong_specular_exponent = float(color.get('exponent'))
            elif color.tag == 'reflection':
                reflection_color = self._parse_color(color[0])
                reflection_color *= float(color.get('factor'))

        return Material(name, ambient_color, diffuse_color,
                        specular_color, phong_specular_exponent,
                        reflection_color)

    def _parse_color(self, color_node):
        return RaytracerColor(int(color_node.get('r'))/255.0,
                              int(color_node.get('g'))/255.0,
                              int(color_node.get('b'))/255.0)

    def _parse_lights(self, lights_node):
        lights = []
        for light_node in lights_node:
            if light_node.tag == 'omnilight':
                light = self._parse_omni_light_source(light_node)
            elif light_node.tag == 'parallellight':
                light = self._parse_parallel_light_source(light_node)
            elif light_node.tag == 'spotlight':
                light = self._parse_spot_light_source(light_node)
            elif light_node.tag == 'fallofflight':
                light = self._parse_falloff_light_source(light_node)
            else:
                raise Exception("Error in create_light_source():\
                                 Unknown light type '" +
                                light_node.tag + "'")
            lights.append(light)
        return lights

    def _parse_omni_light_source(self, light_node):
        if light_node.get('name') is None:
            raise Exception('Error in OmniLightSource(): no name define')
        name = light_node.get('name')
        if light_node.find('vector3d') is None:
            raise Exception('Error in OmniLightSource(): no position defined')
        position = self._parse_vector(light_node.find('vector3d'))
        if light_node.find('color') is None:
            raise Exception('Error in OmniLightSource(): no color defined')
        color = self._parse_color(light_node.find('color'))
        return OmniLightSource(name, position, color)

    def _parse_parallel_light_source(self, light_node):
        if light_node.get('name') is None:
            raise Exception('Error in ParallelLightSource(): no name define')
        name = light_node.get('name')
        if light_node.find('vector3d') is None:
            raise Exception('Error in ParallelLightSource():\
                             no position defined')
        direction = self._parse_vector(light_node.find('vector3d'))
        if light_node.find('color') is None:
            raise Exception('Error in ParallelLightSource(): no color defined')
        color = self._parse_color(light_node.find('color'))
        return ParallelLightSource(name, direction, color)

    def _parse_spot_light_source(self, light_node):
        if light_node.get('name') is None:
            raise Exception('Error in SpotLightSource(): no name define')
        name = light_node.get('name')
        if light_node.get('angle') is None:
            raise Exception('Error in SpotLightSource(): no angle defined')
        angle = float(light_node.get('angle'))
        if light_node.find('position') is None:
            raise Exception('Error in SpotLightSource(): no position defined')
        position = self._parse_vector(light_node.find('position')[0])
        if light_node.find('target') is None:
            raise Exception('Error in SpotLightSource(): no target defined')
        target = self._parse_vector(light_node.find('target')[0])
        if light_node.find('color') is None:
            raise Exception('Error in SpotLightSource(): no color defined')
        color = self._parse_color(light_node.find('color'))
        return SpotLightSource(name, angle, position, target, color)

    def _parse_falloff_light_source(self, light_node):
        if light_node.get('name') is None:
            raise Exception('Error in FallOfLightSource(): no name define')
        name = light_node.get('name')
        if light_node.get('factor') is None:
            raise Exception('Error in FallOfLightSource(): no name define')
        factor = float(light_node.get('factor'))
        if light_node.find('vector3d') is None:
            raise Exception('Error in FallOfLightSource():\
                             no position defined')
        position = self._parse_vector(light_node.find('vector3d'))
        if light_node.find('color') is None:
            raise Exception('Error in FallOfLightSource(): no color defined')
        color = self._parse_color(light_node.find('color'))
        return FalloffLightSource(name, factor, position, color)

    def _parse_vector(self, vector_node):
        return Vector3D(float(vector_node.get('x')),
                        float(vector_node.get('y')),
                        float(vector_node.get('z')))
