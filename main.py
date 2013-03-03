#!/usr/bin/env python2

def main():
    if len(sys.argv) < 2:
        raise Exception('main /path/to/xmlfile output.file')
    print(sys.argv[1])


if __name__ == '__main__':
    main()
