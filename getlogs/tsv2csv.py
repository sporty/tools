#!/usr/bin/env python
# coding=utf-8

import sys
import os
import subprocess
import re
import csv
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=u'TSVからCSVへの変換')
    parser.add_argument(
            'input_filename', metavar='FILENAME', type=argparse.FileType("rb"), nargs='?',
            default=sys.stdin,
            help=u'変換するTSVファイル名。省略時は標準入力。'
            )
    parser.add_argument(
            '-o', '--output', dest='output_filename', type=argparse.FileType("wb"),
            default=sys.stdout,
            help=u'出力CSVファイル名。省略時は標準出力'
            )
    args = parser.parse_args()
    pp.pprint(args)


    tsv_reader = csv.reader(args.input_filename, delimiter='\t', quotechar='|')
    csv_writer = csv.writer(args.output_filename, delimiter=',', quotechar='|', 
                            quoting=csv.QUOTE_MINIMAL)

    max_column = 0
    row_array = []
    for row in tsv_reader:
        csv_writer.writerow(row)

# EOF
