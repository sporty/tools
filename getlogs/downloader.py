#!/usr/bin/env python
# coding=utf-8

import sys
import os
import subprocess
import re
import argparse
import datetime
import pprint
pp = pprint.PrettyPrinter(indent=4, stream=sys.stderr)

import requests
from dateutil import relativedelta


class Downloader(object):
    """
    簡易ダウンローダー
    """

    def auth(self, path, data, method="POST"):
        """
        ユーザー認証
        """
        url = self._base_url+path
        if method == "POST":
            r = requests.post(url, data=data, verify=self._ssl_verify)
        elif method == "GET":
            r = requests.get(url, data=data, verify=self._ssl_verify)

        self._auth_cookies = r.cookies

    def save(self, path, data, method="POST"):
        """
        """
        url = self._base_url+path
        if method == "POST":
            r = requests.post(url, data=data,
                    cookies=self._auth_cookies, verify=self._ssl_verify)
        elif method == "GET":
            r = requests.get(url, data=data,
                    cookies=self._auth_cookies, verify=self._ssl_verify)

        '''
        pp.pprint(r.status_code)
        pp.pprint(r.headers)
        pp.pprint(r.text)
        '''
        # ヘッダからファイル名を取得
        filename = None
        if "content-disposition" in r.headers.keys():
            m = re.search(ur"attachment; filename=(?P<filename>.*)", r.headers['content-disposition'])
            if m:
                filename = m.group("filename").strip("\"")
        if not filename:
            raise Exception(u"ヘッダからファイル名が見つかりませんでした")

        # ファイルに保存
        output_file = os.path.abspath(os.path.join(self._output_directory, filename))
        with open(output_file, "w") as fp:
            fp.write(r.content)

        # ファイル名を保存
        self._filename = output_file

    def get_filename(self):
        """
        """
        return self._filename

    def __init__(self, base_url, output_directory="./", ssl_verify=False):
        """
        """
        # ベースURL
        self._base_url = base_url
        # 保存ディレクトリ
        self._output_directory = output_directory
        # ssl認証
        self._ssl_verify = ssl_verify

if __name__ == "__main__":
    pass

# EOF
