import argparse

import py2048


def main(args):
    py2048.start(args.size)


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Options for py2048 Game.')
    parser.add_argument('--size', '-s', type=int, default=4, required=False,
                        help='The side length of board.')

    main(parser.parse_args())
