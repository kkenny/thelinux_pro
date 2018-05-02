#!/usr/bin/env python
# coding: utf-8

import sys, subprocess

LIQUID_MARKER = "---"
UUID_PREFIX = "uuid: "
UUIDGEN = ("uuidgen", "-r")

def print_uuid():
    uuid = subprocess.check_output(UUIDGEN)
    print(UUID_PREFIX + uuid.strip())

def main(argv):
    seen_footer = False
    seen_uuid = False

    line = sys.stdin.readline()
    if not line.startswith(LIQUID_MARKER):
        seen_footer = seen_uuid = True

    print(line[:-1])
    for line in sys.stdin.readlines():
        line = line[:-1]
        if seen_footer and seen_uuid:
            print(line)
            continue
        if line.startswith(UUID_PREFIX):
            seen_uuid = True
        if line.startswith(LIQUID_MARKER):
            if not seen_uuid:
                print_uuid()
                seen_uuid = True
            seen_footer = True
        print(line)

if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
