#!/usr/bin/env python
# coding=utf-8

import sys
import os
import subprocess
import re
import csv
import argparse
import json
import pprint
pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description=u'CSVの指定した範囲の数値の合計値を出す')
    parser.add_argument(
            'input_filename', metavar='FILENAME', type=argparse.FileType("rb"), nargs='?',
            default=sys.stdin,
            help=u'変換するCSVファイル名。省略時は標準入力。'
            )
    '''
    parser.add_argument(
            '-o', '--output', dest='output_filename', type=argparse.FileType("wb"),
            default=sys.stdout,
            help=u'出力CSVファイル名。省略時は標準出力'
            )
    '''
    parser.add_argument(
            '-l', '--list', dest='safe_list', type=argparse.FileType("rb"),
            default=file("config/sum_span.json"),
            help=u'計算範囲'
            )
    parser.add_argument(
            '-e', '--enc', dest='encoding', type=str,
            default="cp932",
            help=u'入力ファイルのエンコード'
            )
    args = parser.parse_args()
    pp.pprint(args)

    sum_span = json.load(args.safe_list)
    pp.pprint(sum_span)

    csv_reader = csv.reader(args.input_filename, delimiter=',', quotechar='|')

    # 書き出す行
    total = 0
    columns = list(csv_reader)
    for column in columns[sum_span["column"][0]: sum_span["column"][1]]:
        rows = column[sum_span["row"][0]: sum_span["row"][1]]
        for row in rows:
            total += int(row)

    print total
# EOF
