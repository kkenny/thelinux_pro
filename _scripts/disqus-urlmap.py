#!/usr/bin/env python
# coding: utf-8

import re, sys

def url_new(url):
    n = url.strip().replace("github.com", "github.io").replace("//", "/").replace("http:/", "http://").replace("https:/", "https://")
    if not n.endswith("/"):
        n += "/"
    return n

def url_csv(line):
    l = line.strip()
    n = url_new(l)
    return ', '.join((l, n))

if __name__ == '__main__':
    for line in sys.stdin.readlines():
        print(url_csv(line))
