#!/usr/bin/env python3


"""\
Set up to work on a new chapter.
"""


import argparse
import glob
import os
import shutil
import sys

from packt import add_arguments, get_img_dir, get_staging_dir


PREVIOUS = os.path.expanduser(os.path.join(
    '~', 'Dropbox', 'packt', '0297OS', 'first-draft',
    ))
IMAGES = os.path.expanduser(os.path.join(
    '~', 'Dropbox', 'clj-book', 'draft-01',
    ))


def copy_chapter(args):
    srcs = glob.glob(os.path.join(
        args.previous,
        '*_{:02}_FinalDraft*.doc'.format(args.old_chapter),
        ))
    if not srcs:
        raise Exception(
            'No previous final drafts for chapter {}.'.format(args.chapter),
            )

    dest = os.path.join(
        get_staging_dir(args),
        '{}_{:02}_1stDraft.doc'.format(args.isbn, args.chapter),
        )

    print('cp {} {}'.format(srcs[0], dest))
    shutil.copy(srcs[0], dest)


def copy_images(args):
    srcs = glob.glob(os.path.join(
        args.images,
        '*_{:02}_images'.format(args.old_chapter),
        ))
    if not srcs:
        raise Exception(
            'No previous image directory found in {}.'.format(args.images),
            )

    staging = get_staging_dir(args)
    dest = get_img_dir(staging, '{}_{:02}_'.format(args.isbn, args.chapter))

    print('cp -r {} {}'.format(srcs[0], dest))
    shutil.copytree(srcs[0], dest)


def rename_images(args):
    img_dir = get_img_dir(
        get_staging_dir(args),
        '{}_{:02}_'.format(args.isbn, args.chapter),
        )
    for fn in os.listdir(img_dir):
        if not fn.endswith('.png'):
            continue
        src = os.path.join(img_dir, fn)
        (_, _, n) = fn.split('_')
        dest = os.path.join(
            img_dir, '_'.join((args.isbn, str(args.chapter), n)),
            )
        print('mv {} {}'.format(src, dest))
        shutil.move(src, dest)


def bye(args):
    print("Please re-save the chapter file as a DOCX and check that the "
          "formatting hasn't been wiped out.")
    print("Also, delete all comments and accept all revisions.")


def parse_args(argv=None):
    argv = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)

    add_arguments(parser)

    parser.add_argument('-C', '--old-chapter', action='store', default=None,
                        type=int,
                        help="The number of the chapter in the previous book, "
                             "if it's different than the current.")
    parser.add_argument('-p', '--previous', action='store', default=PREVIOUS,
                        type=str,
                        help='The location of the files for the previous '
                             'edition. (Default={}.)'.format(PREVIOUS))
    parser.add_argument('-I', '--images', action='store', default=IMAGES,
                        type=str,
                        help='The location of the image files for the '
                             'previous edition. (Default={}.)'.format(IMAGES))

    args = parser.parse_args(argv)
    if args.old_chapter is None:
        args.old_chapter = args.chapter
    return args


def main(argv=None):
    opts = parse_args(argv)

    copy_chapter(opts)
    copy_images(opts)
    rename_images(opts)

    bye(opts)


if __name__ == '__main__':
    main()
