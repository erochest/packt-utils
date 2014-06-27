#!/usr/bin/env python3


"""\
Copy a file into the next position for a Packt book.
"""


import argparse
import glob
import os
import shutil
import sys

from packt import add_arguments, get_img_dir, get_staging_dir


class FileMover:

    def __init__(self, args):
        self.args = args
        self.prefix = '{}_{:02}_'.format(args.isbn, args.chapter)
        self.img_dir = get_img_dir(get_staging_dir(args), self.prefix)

        self.set_n()

        self.basename = '{}{:02}.png'.format(self.prefix, self.n)
        self.filename = os.path.join(self.img_dir, self.basename)
        self.moved = False

    def set_n(self):
        prefix = self.prefix
        img_dir = self.img_dir
        n = self.args.n

        if n == 0:
            n = 1 + len(glob.glob(os.path.join(img_dir, '*.png')))
            while os.path.isfile(
                    os.path.join(
                        img_dir,
                        '{}{:02}.png'.format(prefix, n))):
                n += 1

        self.n = n

    def move(self):
        sys.stderr.write('{} => {}\n'.format(self.args.input, self.filename))
        if os.path.isfile(self.filename):
            if self.args.force:
                sys.stderr.write('file exists. forcing...\n')
                shutil.copy(self.args.input, self.filename)
                self.moved = True
            else:
                sys.stderr.write('file exists. skipping...\n')
                self.moved = False
        else:
            shutil.copy(self.args.input, self.filename)
            self.moved = True

    def clean_up(self):
        if self.moved and self.args.delete:
            sys.stderr.write('removing {}...\n'.format(self.args.input))
            os.remove(self.args.input)

    def clipboard(self):
        if self.moved:
            sys.stdout.write(self.basename + '\n')
        else:
            sys.stdout.write('ERROR, unable to copy.\n')

    @staticmethod
    def move_file(args):
        mover = FileMover(args)
        mover.move()
        mover.clean_up()
        mover.clipboard()


def parse_args(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)

    add_arguments(parser)

    parser.add_argument('-n', dest='n', action='store', default=0, type=int,
                        help='The number (default is {}, or the next '
                             'available).'.format(0))
    parser.add_argument('-D', '--delete', dest='delete', action='store_true',
                        help='Delete the input file after copying it.')
    parser.add_argument('-f', '--force', dest='force', action='store_true',
                        help='For it to overwrite existing files.')
    parser.add_argument('input', action='store', type=str, metavar='INPUT',
                        help='The input file.')

    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    FileMover.move_file(parse_args())
