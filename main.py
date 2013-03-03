#!/usr/bin/env python2
import sys
import scene


def main():
    if len(sys.argv) < 2:
        raise Exception('main /path/to/xmlfile output.file')
    my_scene = scene.Scene(sys.argv[1])
    my_scene.render(600).show()


if __name__ == '__main__':
    main()
