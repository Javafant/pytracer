import sys
from parser import Parser
import time


def main():
    if len(sys.argv) < 3:
        raise Exception('main /path/to/xmlfile output.file')
    start = time.clock()
    parser = Parser(sys.argv[1])
    scene = parser.parse()
    image = scene.render(600)
    end = time.clock()
    image.save(sys.argv[2])
    print("%.2gs" % (end-start))


if __name__ == '__main__':
    main()
