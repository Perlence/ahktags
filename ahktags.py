#!/usr/bin/env python
from __future__ import print_function

import argparse
from collections import namedtuple
from glob import glob
from itertools import chain
import re


VARIABLE = re.compile(r'^[ \t]*(?P<name>[a-zA-Z0-9_]+)\s*:?=\s*(;?.*)?$', re.M)
LABEL = re.compile(r'^[ \t]*(?P<name>\w+):\s*(;.*)?$', re.M)
FUNCTION = re.compile(r'^[ \t]*(?P<name>\w+)\(.*\)\s*{\s*(;?.*)$', re.M)


TagEntry = namedtuple('TagEntry', 'name, file, address, field, line')


class Tags(object):
    headers = [
        ('_TAG_FILE_FORMAT', 2,
         'extended format; --format=1 will not append ;" to lines'),
        ('_TAG_FILE_SORTED', 1, '0=unsorted, 1=sorted, 2=foldcase'),
        ('_TAG_PROGRAM_AUTHOR', 'Sviatoslav Abakumov',
         'dust.harvesting@gmail.com'),
        ('_TAG_PROGRAM_NAME', 'AHKTags', ''),
        ('_TAG_PROGRAM_URL', 'https://github.com/perlence/ahktags', ''),
        ('_TAG_PROGRAM_VERSION', '0.1', ''),
    ]

    def __init__(self):
        self.entries = []

    def __str__(self):
        return '\n'.join(self._write_headers() + self._write_entries())

    def _write_headers(self):
        return ['!{}\t{}\t/{}/'.format(*header) for header in self.headers]

    def _write_entries(self):
        sorted_entries = sorted(self.entries, key=lambda x: x.name)
        return ['{}\t{}\t{};"\t{}\tline:{}'.format(*entry)
                for entry in sorted_entries]


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--include-vars', action='store_true',
                        help="Include variables in generated tags")
    parser.add_argument('-f', '--file', default='tags',
                        help="Write tags to FILE (use - for std out)")
    parser.add_argument('-R', '--recursive', action='store_true',
                        default=False,
                        help="Process current directory recursively")
    parser.add_argument('--list-kinds', action='store_true',
                        help="Lists the tag kinds")
    parser.add_argument('FILES', nargs='*')
    args = parser.parse_args()

    files = args.FILES
    if args.recursive:
        files += glob('./**/*.ahk')

    tags = Tags()
    for filename in files:
        with open(filename) as fp:
            filename = re.sub(r'^\./', '', filename)
            script = fp.read()
            entries = chain(
                find_entries(FUNCTION, filename, script, 'function'),
                find_entries(LABEL, filename, script, 'label'),
                (find_entries(VARIABLE, filename, script, 'variable')
                 if args.include_vars else []))
            tags.entries += list(entries)

    if not tags.entries:
        return

    if args.file == '-':
        print(tags)
    else:
        with open(args.file, 'w') as fp:
            fp.write(str(tags))


def find_entries(regex, filename, text, field):
    for mo in regex.finditer(text):
        linenumber = len(re.findall(r'(\r\n|\r|\n)', text[:mo.start()])) + 1
        address = mo.group().splitlines()[0].encode('string_escape')
        yield TagEntry(
            name=mo.group('name'),
            file=filename,
            address='/^{}$/'.format(address),
            field=field,
            line=linenumber)


if __name__ == '__main__':
    main()
