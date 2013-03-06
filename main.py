import sys
from PIL import Image
import datetime

from parser import Parser


def main():
    if len(sys.argv) < 3:
        raise Exception('main /path/to/xmlfile output.file')
    outfile = Image.new('RGB', (800, 600))
    for i in range(1):
        start = datetime.datetime.now()
        parser = Parser(sys.argv[1])
        scene = parser.parse()
        pixbuffer = scene.render(600)
        end = datetime.datetime.now()
        print((end-start).total_seconds())
        sys.stdout.flush()
    outfile.putdata(pixbuffer)
    outfile.save(sys.argv[2])


if __name__ == '__main__':
    main()
