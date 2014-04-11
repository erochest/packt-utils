#!/usr/bin/env python


"""\
Zip up all the files for one package.
"""


from __future__ import unicode_literals, print_function, absolute_import

import argparse
import glob
import os
import shutil
import subprocess
import sys
import tempfile
import zipfile


ISBN    = '4139OS'
DRAFT   = 1
ORDINAL = '1st'


class DraftPackager:
    BASEDIR = os.path.expanduser('~/Dropbox/clj-data')

    def __init__(self, args):
        self.args = args
        self.prefix = '{}_{:02}_'.format(args.isbn, args.chapter)
        self.stage_dir = os.path.join(
                self.BASEDIR,
                'draft-{:02}'.format(args.stage),
                )
        self.img_dir = os.path.join(
                self.stage_dir,
                '{}images'.format(self.prefix),
                )
        self.code_dir = os.path.join(
                self.stage_dir,
                '{}code'.format(self.prefix),
                )

        self.tmp_dir = tempfile.mkdtemp()

        self.find_word_draft()

        self.basename = '{}{}Draft.zip'.format(self.prefix, self.args.ordinal)
        self.zip_file = os.path.join(self.stage_dir, self.basename)

    def find_word_draft(self):
        file_tries = [
            os.path.join(self.stage_dir, '{}{}Draft.{}'.format(
                self.prefix, self.args.ordinal, ext,
                ))
            for ext in {'doc', 'docx'}
            ]
        filename = None

        for fn in file_tries:
            if os.path.exists(fn):
                filename = fn
                break
        else:
            raise Exception('No Word draft found.\n{}'.format(file_tries))

        self.word_draft = filename
        return filename

    def zip_code(self):
        cmd = ' '.join(
            ['git', 'clone', self.args.git_repo, self.args.isbn],
            )
        retcode = subprocess.call(cmd, shell=True, cwd=self.tmp_dir)
        if retcode != 0:
            raise Exception('ERROR ON "{}"'.format(cmd))
        full_chapter_dir = os.path.join(
                self.tmp_dir, self.args.isbn, self.args.chapter_dir,
                )
        if not os.path.exists(self.code_dir):
            os.makedirs(self.code_dir)
        zip_filename = os.path.join(
                self.code_dir, '{}code.zip'.format(self.prefix),
                )

        with zipfile.ZipFile(zip_filename, 'w', zipfile.ZIP_DEFLATED) as zf:
            for (root, dirs, files) in os.walk(full_chapter_dir):
                zip_root = root.replace(full_chapter_dir, self.args.chapter_dir)
                for fn in files:
                    zf.write(os.path.join(root, fn), os.path.join(zip_root, fn))

        ls_zip('CODE ZIP:', zip_filename)

    def package(self):
        with zipfile.ZipFile(self.zip_file, 'w', zipfile.ZIP_DEFLATED) as zf:
            zf.write(self.word_draft, os.path.basename(self.word_draft))
            self.__package_dir(zf, self.img_dir, '*.png')
            self.__package_dir(zf, self.code_dir, '*.zip')

    def __package_dir(self, zip_file, basedir, pattern):
        basename = os.path.basename(basedir)
        for fn in glob.glob(os.path.join(basedir, pattern)):
            zip_file.write(fn, os.path.join(basename, os.path.basename(fn)))

    def clean_up(self):
        shutil.rmtree(self.tmp_dir, True)

    @staticmethod
    def package_stage(args):
        mover = DraftPackager(args)
        try:
            mover.zip_code()
            mover.package()
        finally:
            mover.clean_up()

        ls_zip('OUTPUT', mover.zip_file)


def ls_zip(title, zip_file):
    print()
    print(title)
    subprocess.call(['unzip', '-l', zip_file])


def parse_args(argv=None):
    argv   = argv if argv is not None else sys.argv[1:]
    parser = argparse.ArgumentParser(description=__doc__)

    parser.add_argument('-i', '--isbn', dest='isbn', action='store',
                        default=ISBN, type=unicode,
                        help='The ISBN for the project (default={}).'.format(ISBN))
    parser.add_argument('-s', '--stage', dest='stage', action='store',
                        default=DRAFT, type=int,
                        help='The stage (default={}).'.format(DRAFT))
    parser.add_argument('-o', '--ordinal', dest='ordinal', action='store',
                        default=ORDINAL, type=unicode,
                        help='The draft (default={}).'.format(ORDINAL))
    parser.add_argument('-c', '--chapter', dest='chapter', action='store',
                        required=True, type=int,
                        help='The chapter for the image.')
    parser.add_argument('-g', '--git-repo', dest='git_repo', action='store',
                        required=True, type=unicode,
                        help='The git repo to clone for the code.')
    parser.add_argument('-C', '--chapter-dir', dest='chapter_dir', action='store',
                        required=False, type=unicode,
                        default=os.path.basename(os.getcwdu()),
                        help='The chapter directory inside the git repo to zip up '
                             '(default={}).'.format(os.path.basename(os.getcwdu())))

    args = parser.parse_args(argv)
    return args


if __name__ == '__main__':
    DraftPackager.package_stage(parse_args())
