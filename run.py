#!/usr/bin/env python3

from argparse import ArgumentParser
from PIL import Image
from sys import stdin
from os import listdir
from io import BytesIO
from importlib import import_module
from config import ALGORITHMS_PATH

algorithms = [a.split('.')[0] for a in listdir(ALGORITHMS_PATH)
              if not a.startswith('__')]


def prepare_image(image, sizes, dither=False):
    image.thumbnail(sizes)
    if dither:
        gray = image.convert('1')
    else:
        gray = image.convert('LA')
    bw = gray.point(lambda x: 0 if x < 128 else 255)
    if dither:
        values = list(bw.getchannel('1').getdata())
    else:
        values = list(bw.getchannel('L').getdata())
    return values, bw.size


if __name__ == '__main__':
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file',
                        help='Image path. Reads from STDIN if not specified')

    parser.add_argument('-b', '--algorithm',
                        dest='algorithm', type=str,
                        help='Specifies the algorithm',
                        choices=algorithms)
    parser.add_argument('-d', action='store_true', dest='dithering',
                        help='Dithering on/off')
    parser.add_argument('-n', action='store_true', dest='negative',
                        help='Negative on/off')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Verbosity on/off')
    parser.add_argument('-x', type=int, dest='width', default=128,
                        help='Desired width')
    parser.add_argument('-y', type=int, dest='height', default=128,
                        help='Desired height')
    args = parser.parse_args()

    if args.input_file:
        img = Image.open(args.input_file, mode="r")
    else:
        data = stdin.buffer.read()
        buffer = BytesIO(data)
        img = Image.open(buffer, mode="r")
    values, size = prepare_image(
        img, (args.width, args.height), args.dithering
    )

    algorithms = import_module('algorithms')
    encoder_class = import_module('algorithms.' + args.algorithm)
    if args.verbose:
        print('Source: {}'.format(args.input_file or '<STDIN>'))
        print('Size: {}×{}'.format(size[0], size[1]))
        print('Dithering: {}'.format(args.dithering))
        print('Negative: {}'.format(args.negative))
        print('Algorithm: "{}"'.format(args.algorithm))
    encoder_class.Encoder.encode(values, size, args.negative)
