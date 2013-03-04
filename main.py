#!/usr/bin/env python2
import sys
import scene
import time

def main():
    if len(sys.argv) < 2:
        raise Exception('main /path/to/xmlfile output.file')
    start = time.clock()
    my_scene = scene.Scene(sys.argv[1])
    image = my_scene.render(600)
    end = time.clock()
    image.save(sys.argv[2])
    print "%.2gs" % (end-start)


if __name__ == '__main__':
    main()
