

def parse(lights_node):
    lights = []
    for node in lights_node:
        lights.append(Lights(node))

class Light:
    def __init__(self, node):
        #omg subclasses
        pass
