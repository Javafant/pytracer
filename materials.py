def get_material_by_name(name, materials):
    '''
        :param str name: name of the wanted material
        :returns: a material with strName as name or non if not found
        :rtype: Material  or None if not found
    '''
    for m in materials:
        if m.name == name:
            return m
    return None


class Material:
    ''' it's a material
    '''

    def __init__(self, name, ambient_color, diffuse_color,
                 specular_color, phong_specular_exponent,
                 reflection_color):
        self.name = name
        self.ambient_color = ambient_color
        self.diffuse_color = diffuse_color
        self.specular_color = specular_color
        self.phong_specular_exponent = phong_specular_exponent
        self.reflection_color = reflection_color
