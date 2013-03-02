import vector

class Camera:
    def __init__(self,cam_node):
        for node in cam_node:
            if node.tag == 'position':
                self.position = vector.Vector3D(float(node[0].attrib['x']),
                                                float(node[0].attrib['y']),
                                                float(node[0].attrib['z']))
            elif node.tag == 'lookat':
                self.target = vector.Vector3D(float(node[0].attrib['x']),
                                                float(node[0].attrib['y']),
                                                float(node[0].attrib['z']))
            elif node.tag == 'upvector':
                self.up_vector = vector.Vector3D(float(node[0].attrib['x']),
                                                float(node[0].attrib['y']),
                                                float(node[0].attrib['z']))
            elif node.tag == 'options':
                self.near_clipping = float(node.attrib['nearclipping'])
                self.viewing_angle = float(node.attrib['fov'])
                self.aspect_ratio = float(node.attrib['aspectratio'])
