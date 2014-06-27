

import os


BASEDIR = os.path.expanduser('~/Dropbox/packt')
ISBN = '0297OS'
STAGE = 1


def get_staging_dir(args):
    return os.path.join(
        BASEDIR,
        args.isbn,
        'ed{:02}.draft{:02}'.format(args.edition, args.stage),
        )


def get_data_dir(staging_dir, prefix, kind):
    return os.path.join(staging_dir, prefix + kind)


def get_img_dir(staging_dir, prefix):
    return get_data_dir(staging_dir, prefix, 'images')


def get_code_dir(staging_dir, prefix):
    return get_data_dir(staging_dir, prefix, 'code')


def add_arguments(parser):
    parser.add_argument('-i', '--isbn', dest='isbn', action='store',
                        default=ISBN, type=unicode,
                        help='The ISBN for the project '
                             '(default={}).'.format(ISBN))
    parser.add_argument('-e', '--edition', dest='edition', action='store',
                        default=2, type=int,
                        help='The edition of this book (default=1).')
    parser.add_argument('-s', '--stage', dest='stage', action='store',
                        default=STAGE, type=int,
                        help='The stage (default={}).'.format(STAGE))
    parser.add_argument('-c', '--chapter', dest='chapter', action='store',
                        required=True, type=int,
                        help='The chapter for the image.')
