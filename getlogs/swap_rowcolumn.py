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

import requests
import dateutil

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=u'CSVの行列変換')
    parser.add_argument(
            'input_filename', metavar='FILENAME', type=argparse.FileType("rb"), nargs='?',
            default=sys.stdin,
            help=u'変換するCSVファイル名。省略時は標準入力。'
            )
    parser.add_argument(
            '-o', '--output', dest='output_filename', type=argparse.FileType("wb"),
            default=sys.stdout,
            help=u'出力CSVファイル名。省略時は標準出力'
            )
    args = parser.parse_args()
    pp.pprint(args)


    csv_reader = csv.reader(args.input_filename, delimiter=',', quotechar='|')
    csv_writer = csv.writer(args.output_filename, delimiter=',', quotechar='|', 
                            quoting=csv.QUOTE_MINIMAL)

    # 最大の列の数を調べる
    max_column = 0
    row_array = []
    for row in csv_reader:
        row_array.append(row)
        if max_column < len(row):
            max_column = len(row)

    for current_column in range(max_column):
        tmp = []
        for row in row_array:
            if current_column >= len(row):
                tmp.append("")
            else:
                tmp.append(row[current_column])
        csv_writer.writerow(tmp)

# EOF
