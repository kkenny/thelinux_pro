#!/usr/bin/env bash
# tidy wrapper
# Copyright 2011 Ali Polatel <polatel@gmail.com>
# Distributed under the terms of the GNU General Public License v2

log="${XMLLINT_LOG:-./tidy.log}"
srcs="${@:-.}"

tidy_bin=$(which tidy 2>/dev/null)
if [[ -z "$tidy_bin" ]]; then
    echo "no tidy in PATH" >&2
    exit 127
fi

xtidy() {
    "$tidy_bin" -utf8 "$@"
}

count_fail=0
count_html=0
count_xml=0
while read f; do
    case "$f" in
    *.html)
        opts=""
        (( count_html++ ))
        ;;
    *.xml)
        opts="-xml"
        (( count_xml++ ))
        ;;
    *)
        continue
        ;;
    esac

    xtidy -q $opts "$f" >/dev/null 2>&1
    if [[ $? != 0 ]]; then
        (( count_fail++ ))
        echo "-- FAIL:$fail path:$f" >> "$log"
        xtidy -e -q $opts "$f" >>"$log" 2>&1
    fi
done < <(find "$srcs" -type f)

echo "Processed $count_html html and $count_xml xml files" >&2
if [[ $count_fail > 0 ]]; then
    echo "Detected $count_fail non-valid files, details are in $log" >&2
    exit 1
fi

true
