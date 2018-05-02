---
layout: post
title: Batch tagging of audio files from the command line
categories: [en, blog]
tags: [audio, afprint, musicbrainz, musicdns]
uuid: f4a98db8-2b3a-4347-9a8e-ab2ab48e5cf1
---

As many of you know [MusicDNS](http://en.wikipedia.org/wiki/MusicDNS) is an
acoustic fingerprinting service and a software development kit provided by
MusicIP. The fingerprinting client library that looks up and identifies audio
files based on existing fingerprints is called
[libofa](http://code.google.com/p/musicip-libofa/).
[MusicBrainz](http://musicbrainz.org/) has a great audio tagger called
[Picard](http://musicbrainz.org/doc/MusicBrainz_Picard) which can tag audio
files by querying this [MusicDNS](http://en.wikipedia.org/wiki/MusicDNS)
service.

There is, however, a simple problem.
[Picard](http://musicbrainz.org/doc/MusicBrainz_Picard) is a
[GUI](http://en.wikipedia.org/wiki/Graphical_user_interface) and thus doesn't
allow batch tagging of audio files from command line.

Hence I decided to write my own tool for generating acoustic fingerprints and
for querying [MusicDNS](http://en.wikipedia.org/wiki/MusicDNS) service. I've
chosen to use [libsndfile](http://www.mega-nerd.com/libsndfile/) to do the
decoding as [libofa](http://code.google.com/p/musicip-libofa/) expects raw audio
data. [libsndfile](http://www.mega-nerd.com/libsndfile/) is a C library for
reading and writing files containing sampled sound through one standard library
interface. It's pretty easy to use and its
[API](http://en.wikipedia.org/wiki/API) hides most of the low-level details from
the programmer.

The tool is named [afprint](http://github.com/alip/afprint), released under
[GPLv2](http://en.wikipedia.org/wiki/GPLv2#Version_2). Following the
[UNIX](http://en.wikipedia.org/wiki/Unix) philosophy it just does one thing,
calculation of acoustic fingerprint and duration of the given audio file.

Usage is simple:

    alip@harikalardiyari> afprint -h
    afprint-0.1.0-7b17577 audio fingerprinting tool
    Usage: afprint [-hVv0] <infile>

    Options:
        -h, --help      Display usage and exit
        -V, --version   Display version and exit
        -v, --verbose   Be verbose
        -0, --print0    Delimit path and fingerprint by null character instead of space
    If <infile> is '-' afprint reads from standard input.
    alip@harikalardiyari> afprint -v sample.ogg
    [dump_print.294] Format: OGG (OGG Container format)
    [dump_print.295] Frames: 2188368
    [dump_print.296] Channels: 1
    [dump_print.297] Samplerate: 44100Hz
    [dump_print.298] Duration: 49735ms
    [dump_print.302] essential frames: 5953500 > frames: 2188368, adjusting
    sample.ogg 49735 ARaJDAgL...

[afprint](http://github.com/alip/afprint) decodes the audio data using
[libsndfile](http://www.mega-nerd.com/libsndfile/) and feeds it to
[libofa](http://code.google.com/p/musicip-libofa/). It also calculates the
duration of the audio file and prints them in format:
`FILENAME DURATION FINGERPRINT`

Reading from standard input is tricky because pipes aren't seekable thus it's
not possible to calculate the duration of the audio file. For this reason, when
the audio data is fed via standard input, when `<infile>` is `-`,
[afprint](http://github.com/alip/afprint) saves this data into a temporary file
and reads from it. This makes it possible to calculate acoustic fingerprints of
[Mp3](http://en.wikipedia.org/wiki/Mp3) files, which
[libsndfile](http://www.mega-nerd.com/libsndfile/) doesn't
[support](http://www.mega-nerd.com/libsndfile/FAQ.html#Q020), easily.

    alip@harikalardiyari> mpg123 -q --au - 01_san_francisco.mp3|afprint -v -
    [wav.c:388] warning: Cannot rewind AU file. File-format isn't fully conform now.
    [wav.c:388] warning: Cannot rewind AU file. File-format isn't fully conform now.
    [dump_print.294] Format: AU (Sun/NeXT)
    [dump_print.295] Frames: 8000111
    [dump_print.296] Channels: 2
    [dump_print.297] Samplerate: 44100Hz
    [dump_print.298] Duration: 181820ms
    /dev/stdin.au 181820 AQMZN...

Note the `--au` option passed to [mpg123](http://www.mpg123.de/) as `--wav`
doesn't work.

So far so good, now we need a tool to query the
[MusicDNS](http://en.wikipedia.org/wiki/MusicDNS) server to find out the
[PUID](http://en.wikipedia.org/wiki/Portable_Unique_IDentifier) of the audio
file and query [MusicBrainz](http://musicbrainz.org/) to get the audio tags.

I've written a simple [Perl](http://www.perl.org/) script to do the job. The
script, which has the name
[puidlookup](http://github.com/alip/afprint/blob/master/scripts/puidlookup.in),
reads audio fingerprints from standard input and queries the
[MusicDNS](http://en.wikipedia.org/wiki/MusicDNS) server. Optionally it can
query [MusicBrainz](http://musicbrainz.org/) as well to receive the tags.

Here are the requirements:

- [Perl](http://www.perl.org) (obviously)
- [libwww-perl](http://search.cpan.org/~gaas/libwww-perl/)
- [XML-Simple](http://search.cpan.org/~grantm/XML-Simple/)
- [WebService-MusicBrainz](http://search.cpan.org/~bfaist/WebService-MusicBrainz/)
- [Time-HiRes](http://search.cpan.org/~jhi/Time-HiRes/)

Usage is simple, just pipe [afprint](http://github.com/alip/afprint)'s output to
[puidlookup](http://github.com/alip/afprint/blob/master/scripts/puidlookup.in).

    alip@harikalardiyari> puidlookup -h
    Usage: puidlookup [-hVv0]
        -h, --help          Display usage and exit
        -V, --version       Display version and exit
        -v, --verbose       Be verbose
        -0, --null          Expect input is null delimited
        -m, --musicbrainz   Look up PUIDs from MusicBrainz
                            (requires WebService-MusicBrainz)
        -l, --limit         Limit results to the given number
    puidlookup reads filename, duration and audio fingerprint from standard input

The `--null` option responds to [afprint](http://github.com/alip/afprint)'s
`--print0` option. These options are useful if filenames have spaces or other
weird characters in it.

By default it only queries [MusicDNS](http://en.wikipedia.org/wiki/MusicDNS):

    alip@harikalardiyari> afprint 04sheep.ogg | puidlookup
    ARTIST='Pink Floyd'
    TITLE='Sheep'
    PUID=930806c1-e1e0-588a-b7de-2dacb1b8b11e

The `--musicbrainz` option can be used to query
[MusicBrainz](http://musicbrainz.org/):

    alip@harikalardiyari> afprint 04sheep.ogg | puidlookup --musicbrainz
    PUID=930806c1-e1e0-588a-b7de-2dacb1b8b11e
    TRACKID=431a85dd-e22b-4626-91c9-c0abb8058d3f
    ARTISTID=83d91898-7763-47d7-b03b-b92132375c47
    ARTIST='Pink Floyd'
    TITLE='Sheep'
    TRACK=4
    ALBUM='Animals'

The output is quoted so it's safe to pass to `eval`, making it easy to integrate
with shell scripts.

Last step is writing a tagger script to tag audio files. I've written a shell script
called [ofatag](http://github.com/alip/afprint/blob/master/scripts/ofatag) which
uses [envtag](http://github.com/alip/envtag). It recognizes
[Mp3](http://en.wikipedia.org/wiki/Mp3) files using the `file` command and
decodes using `mpg123`, other formats are directly fed to
[afprint](http://github.com/alip/afprint).

Now, to tag your files using MusicBrainz web services just do  
`ofatag /path/to/music/*.mp3 /path/to/music/*.ogg`  
etc.

I haven't released a version yet because it's all pretty new and needs testing.
So please test it and report back! Any comments, thoughts, patches are
appreciated.
