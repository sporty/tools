#!/usr/bin/env python
# coding=utf-8

import sys
import os
import subprocess
import re
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=u'日付付きファイル名を本日の日付でコピー')
    parser.add_argument(
                'path', metavar='PATH', type=str, nargs='+',
                help=u'コピーするファイル'
            )
    parser.add_argument(
                '-F', '--format', dest='format',
                default=None,
                help=u'日付フォーマットを強制的に指定する'
            )
    parser.add_argument(
                '-f', '--force', dest='force', action='store_true',
                default=False,
                help=u'確認せずにコピー'
            )
    args = parser.parse_args()

    pp.pprint(args)

    date_pattern = {
            ur"(?P<year>[0-9]{4})(?P<month>[0-9]{2})(?P<date>[0-9]{2})": ur"%y%m%d",
            ur"(?P<year>[0-9]{4})_(?P<month>[0-9]{2})_(?P<date>[0-9]{2})": ur"%y_%m_%d",
            }

    for path in args.path:
        fullpath = os.path.abspath(unicode(path, "utf-8"))
        (dirname, filename) = os.path.split(fullpath)
        print dirname
        print filename
        # フォーマット決定
        if args.format:
            # 引数で指定されている場合は
            if args.format in date_pattern.keys:
                date_format = date_patten[args.format]
            else:
                raise Exception(u"%sは定義されていません" % (args.format, ))
            date_format = args.format
        else:
            # 予め用意されたパターンからフォーマットを決定する
            for (key, value) in date_pattern.items():
                m = re.search(key, filename)
                if m:
                    date_regex = key
                    date_format = value

        # ファイル名決定
        print date_regex
        print date_format
        new_filename = u""

        # ユーザーの許可
        if not args.force:
            #res = raw_input(u"%sを元に%sを作成します。よろしいですか？" % (filename, new_filename))
            res = raw_input("?")
            if res != "y":
                continue

        # コピー実行
        print u"cp %s %s" % (filename, new_filename)
        #p = subprocess.Popen(["cp", path, new_filename])

# EOF
