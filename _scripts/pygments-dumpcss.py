#!/usr/bin/env python
# coding: utf-8

import sys
from pygments.formatters import HtmlFormatter

def main():
    if len(sys.argv) >= 2:
        s = sys.argv[1]
    else:
        s = 'default'

    f = HtmlFormatter(nobackground=True, style=s)

    print("/* pygments.styles.%s */" % s)
    for line in f.get_style_defs().splitlines():
        print(".%s %s" % (f.cssclass, line))

if __name__ == '__main__':
    main()
