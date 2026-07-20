#!/usr/bin/env python3

from argparse import ArgumentParser, ArgumentTypeError
from importlib import import_module
from io import BytesIO
from sys import stdin, stderr

from config import ALGORITHMS_PATH


def discover_algorithms():
    algorithms = []
    for path in ALGORITHMS_PATH.glob('*.py'):
        if path.name.startswith('__'):
            continue
        try:
            load_encoder(path.stem)
        except (ImportError, ValueError):
            continue
        algorithms.append(path.stem)
    return sorted(algorithms)


def positive_int(value):
    try:
        parsed = int(value)
    except ValueError as exc:
        raise ArgumentTypeError(f'{value!r} is not an integer') from exc
    if parsed <= 0:
        raise ArgumentTypeError('must be a positive integer')
    return parsed


def prepare_image(image, sizes, dither=False):
    image = image.copy()
    image.thumbnail(sizes)
    if dither:
        gray = image.convert('1')
        bw = gray.point(lambda x: 0 if x < 128 else 255)
        values = list(bw.getdata())
    else:
        gray = image.convert('LA')
        bw = gray.point(lambda x: 0 if x < 128 else 255)
        values = list(bw.getchannel('L').getdata())
    return values, bw.size


def load_encoder(algorithm):
    module = import_module(f'algorithms.{algorithm}')
    encoder = getattr(module, 'Encoder', None)
    if encoder is None or not callable(getattr(encoder, 'encode', None)):
        raise ValueError(f'Algorithm {algorithm!r} does not expose Encoder.encode')
    return encoder


def build_parser():
    algorithms = discover_algorithms()
    parser = ArgumentParser()
    parser.add_argument('-i', '--input-file', dest='input_file',
                        help='Image path. Reads from STDIN if not specified')
    parser.add_argument('-b', '--algorithm',
                        dest='algorithm', type=str, required=True,
                        help='Specifies the algorithm',
                        choices=algorithms)
    parser.add_argument('-d', action='store_true', dest='dithering',
                        help='Dithering on/off')
    parser.add_argument('-n', action='store_true', dest='negative',
                        help='Negative on/off')
    parser.add_argument('-v', action='store_true', dest='verbose',
                        help='Verbosity on/off')
    parser.add_argument('-x', type=positive_int, dest='width', default=128,
                        help='Desired width')
    parser.add_argument('-y', type=positive_int, dest='height', default=128,
                        help='Desired height')
    return parser


def open_image(input_file):
    from PIL import Image, UnidentifiedImageError

    try:
        if input_file:
            return Image.open(input_file, mode='r')
        data = stdin.buffer.read()
        return Image.open(BytesIO(data), mode='r')
    except FileNotFoundError:
        print(f'Error: image file not found: {input_file}', file=stderr)
    except UnidentifiedImageError:
        source = input_file or '<STDIN>'
        print(f'Error: could not identify image data from {source}', file=stderr)
    return None


def main():
    parser = build_parser()
    args = parser.parse_args()

    img = open_image(args.input_file)
    if img is None:
        return 1

    values, size = prepare_image(
        img, (args.width, args.height), args.dithering
    )

    try:
        encoder_class = load_encoder(args.algorithm)
    except ValueError as exc:
        print(f'Error: {exc}', file=stderr)
        return 1

    if args.verbose:
        print('Source: {}'.format(args.input_file or '<STDIN>'))
        print('Size: {}×{}'.format(size[0], size[1]))
        print('Dithering: {}'.format(args.dithering))
        print('Negative: {}'.format(args.negative))
        print('Algorithm: "{}"'.format(args.algorithm))

    print(encoder_class.encode(values, size, args.negative))
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
