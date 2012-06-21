#!/usr/bin/env python
# coding=utf-8

import os
import subprocess
import re
import argparse
import pprint
pp = pprint.PrettyPrinter(indent=4)


class MacPath(object):
    """
    内部でMacパスによる保存を行い、Windows形式のパスを返すことも出来るクラス
    """

    def get_server_path(self, dirname):
        """
        Macのマウント情報を解析し、指定したディレクトリにマウントしているServerとパスを返す

        @param dirname ディレクトリ名
        """

        bufsize = 1024
        p = subprocess.Popen(["df"], shell=True, bufsize=bufsize,
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        (child_stdout, child_stdin) = (p.stdout, p.stdin)
        lines = child_stdout.read().split("\n")
        #pp.pprint(lines)
        for line in lines:
            columns = line.split()
            if len(columns) < 6:
                continue
            if columns[5] != dirname:
                continue

            m = re.search(ur"//(?P<username>[^@]+)@(?P<servername>.*)/(?P<dirname>.*)", columns[0])
            if m:
                #pp.pprint(m.groups())
                return ur"\\%s\%s" % (m.group("servername"), m.group("dirname"))
            else:
                continue

    def get_mount_point(self, servername, dirname):
        """
        Macのマウント情報を解析し、指定したServerの指定したパスをマウントしているディレクトリを返す

        @param servername サーバー名
        @param dirname ディレクトリ名
        """

        bufsize = 1024
        p = subprocess.Popen(["df"], shell=True, bufsize=bufsize,
                  stdin=subprocess.PIPE, stdout=subprocess.PIPE, close_fds=True)
        (child_stdout, child_stdin) = (p.stdout, p.stdin)
        lines = child_stdout.read().split("\n")
        #pp.pprint(lines)
        for line in lines:
            columns = line.split()
            if len(columns) < 6:
                continue

            m = re.search(ur"//(?P<username>[^@]+)@(?P<servername>.*)/(?P<dirname>.*)", columns[0])
            if m:
                #pp.pprint(m.groups())
                if m.group("servername").startswith(servername.lower()) and m.group("dirname").startswith(dirname.upper()):
                    return columns[5]
            else:
                continue

    def set_win_path(self, path):
        """
        """
        p = os.path.normpath(path)
        p = p.replace(u"\\" ,"/")

        names = p[1:].split("/")
        if len(names) < 3:
            raise Exception("invalid path : %s" % (self._path, ))

        mount_point = mp.get_mount_point(names[0], names[1])
        if mount_point:
            self._path =  u"%s/%s" % (mount_point, "/".join(names[2:]))
        else:
            raise Exception("can't find mount point : /%s/%s" % (names[0], names[1]))

    def get_win_path(self):
        """
        """
        names = self._path[1:].split("/")
        if names[0] == "Volumes":
            server_path = mp.get_server_path("/Volumes/"+names[1])
            return u"%s\\%s" % (server_path, "\\".join(names[2:]))

    def set_mac_path(self, path):
        """
        """
        self._path = os.path.abspath(path)

    def get_mac_path(self):
        """
        """
        return self._path

    def __init__(self):
        """
        コンストラクタ
        """
        self._path = ""


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description=u'MacとWindowsのパス変換')
    parser.add_argument(
            'path', metavar='PATH', type=str, nargs='+',
            help=u'変換するパス'
            )
    parser.add_argument(
            '-m', '--mac2win', dest='mac2win', action='store_true',
            default=False,
            help=u'Macのパスを取得したい場合に指定する。標準出力にパスが出力されるだけ。'
            )
    args = parser.parse_args()

    #pp.pprint(args)
    mp = MacPath()
    if args.mac2win:
        mp.set_mac_path(unicode(args.path[0], "utf-8"))
        new_path = mp.get_win_path()
        print new_path
    else:
        mp.set_win_path(unicode(args.path[0], "utf-8"))
        new_path = mp.get_mac_path()
        print new_path
        p = subprocess.Popen(["open", new_path])

# EOF
