import color


def parse(mat_node):
    materials = []
    for node in mat_node:
        materials.append(Material(node))
    return materials


class Material:
    ''' it's a material
    '''

    def __init__(self, node):
        self.name = node.get('name')
        for c in node:
            if c.tag == 'ambient':
                self.ambient_color = color.parse(c[0])
                self.ambient_color *= float(c.get('factor'))
            elif c.tag == 'diffuse':
                self.diffuse_color = color.parse(c[0])
                self.diffuse_color *= float(c.get('factor'))
            elif c.tag == 'specular':
                self.specular_color = color.parse(c[0])
                self.specular_color *= float(c.get('factor'))
                self.phong_specular_exponent = float(c.get('exponent'))
            elif c.tag == 'reflection':
                self.reflection_color = color.parse(c[0])
                self.reflection_color *= float(c.get('factor'))
