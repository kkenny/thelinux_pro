#!/bin/sh

exec pgn-extract -Wuci -C -N -V -w5000 --nomovenumbers --nochecks --noresults --notags "$@"
