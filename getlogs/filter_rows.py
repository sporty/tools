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

    parser = argparse.ArgumentParser(description=u'CSVをフィルタリングし、許可した行のみにする')
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
    parser.add_argument(
            '-l', '--list', dest='safe_list', type=argparse.FileType("rb"),
            default=file("config/safe_rows_normal.json"),
            help=u'許可リストJSONファイル名。（columnインデックスを添字とする正規表現文字列の辞書）'
            )
    parser.add_argument(
            '-e', '--enc', dest='encoding', type=str,
            default="cp932",
            help=u'入力ファイルのエンコード'
            )
    args = parser.parse_args()
    pp.pprint(args)

    safe_regex = json.load(args.safe_list)
    pp.pprint(safe_regex)

    csv_reader = csv.reader(args.input_filename, delimiter=',', quotechar='|')
    csv_writer = csv.writer(args.output_filename, delimiter=',', quotechar='|', 
                            quoting=csv.QUOTE_MINIMAL)

    # 書き出す行
    labels = next(csv_reader)
    csv_writer.writerow(labels)
    for row in csv_reader:
        match_flag = False
        for (key, regex) in safe_regex.items():
            u_value = unicode(row[int(key)], args.encoding)
            m = re.match(regex, u_value)
            if m:
                match_flag = True
                break
        if match_flag:
            csv_writer.writerow(row)

# EOF
