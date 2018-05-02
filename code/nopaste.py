#!/usr/bin/python
# vim: set et ts=4 sts=4 tw=79 :
# Script to generate nopaste urls
# This is a rewrite of Aron Griffis' script in python
# Written by Ali Polatel
# Released under the GNU General Public License v2

import os
import urllib
import urllib2
import getopt
import sys
import cgi
import commands

colors = {'bold': '\x1b[1m',
        'normal':'\x1b[0m',
        'blue':'\x1b[34m',
        'green':'\x1b[32m',
        'red':'\x1b[31m',
        'cyan':'\x1b[36m',
}

def usage():
    print "%(bold)s%(cyan)snopaste script for rafb.net/paste%(normal)s" % colors
    print "%(bold)susage :%(normal)s %(bold)s%(green)snopaste.py %(normal)s%(bold)s%(blue)s[options]%(normal)s" % colors
    print "%(bold)sOptions:%(normal)s" % colors
    print "\t%(bold)s%(blue)s-h,--help%(normal)s\tYou're looking at it" % colors
    print "\t%(bold)s%(blue)s-l,--language%(normal)s\tSet language ( defaults to 'Plain Text')" % colors
    print "\t%(bold)s%(blue)s-n,--nick%(normal)s\tnickname" % colors
    print "\t%(bold)s%(blue)s-d,--desc%(normal)s\tdescription" % colors
    print "\t%(bold)s%(blue)s-v,--verbose%(normal)s\tverbose mode" % colors 
    print "\t%(bold)s%(blue)s-c,--nocolor%(normal)s\tsupress coloring of output" % colors
    print "\t%(bold)s%(blue)s-x%(normal)s\t\tNopaste from X selection instead of stdin (using xclip or xcut)" % colors

def xclip():
    if os.path.exists("/usr/bin/xclip"):
        cmd = "/usr/bin/xclip -o 2>/dev/null"
    elif os.path.exits("/usr/bin/xcut"):
        cmd = "/usr/bin/xcut -p 2>/dev/null"
    else:
        print "%(bold)s%(red)sCouldn't find xclip or xcut%(normal)s" % colors
        sys.exit(1)
    return commands.getoutput(cmd)

class Nopaste:

    def __init__(self,txt,verbose,lang,color,nick,desc):
        """ Initialize the class """
        self.url = "http://www.rafb.net/paste/paste.php"
        self.txt = txt
        self.verbose = verbose
        self.lang = lang
        self.color = color
        self.nick = nick
        self.desc = desc
        # Suppress coloring if -n is specified
        if not color:
            for key in colors.keys():
                colors[key]=""
        # Close stdout if not verbose
        if not self.verbose:
            sys.stdout.close()
            sys.stdout = open("/dev/null","a+")
        print "%(bold)s%(cyan)sVerbose mode%(normal)s" % colors
        print ("%(bold)s%(cyan)sLanguage : %(normal)s %(bold)s%(green)s %%s %(normal)s" % colors) % self.lang
        print ("%(bold)s%(cyan)sNick     : %(normal)s %(bold)s%(green)s %%s %(normal)s" % colors) % self.nick
        if not self.desc == "":
            print ("%(bold)s%(cyan)sDescription : %(normal)s %(bold)s%(green)s %%s %(normal)s" % colors) % self.desc
        else:
            print "%(bold)s%(cyan)sDescription : %(normal)s %(bold)s%(red)s None %(normal)s" % colors

    def params_encode(self):
        """ Encode the parameters """
        print "%(bold)s%(cyan)sSetting headers %(normal)s" % colors
        self.headers = {"Content-Type" : "application/x-www-form-urlencoded"}
        # TODO check the length of nickname and description
        print "%(bold)s%(cyan)sEncoding parameters %(normal)s" % colors
        if text == "":
            sys.stderr.write("%(bold)s%(red)sNothing to paste!%(normal)s" % colors)
        plist= { 'lang' : cgi.escape(self.lang),
                'nick' : cgi.escape(self.nick),
                'desc' : cgi.escape(self.desc),
                'text' : cgi.escape(self.txt),
        }
        self.params= urllib.urlencode(plist)

    def paste(self):
        """ Main function  """
        print "%(bold)s%(cyan)sSending the request" % colors
        req = urllib2.Request(self.url,self.params,self.headers)
        handle = urllib2.urlopen(req)
        print "Reading...%(normal)s" % colors
        if not self.verbose:
            sys.stdout = open("/dev/stdout","a+")
        print ("%(bold)s%(green)s%%s%(normal)s" % colors) % handle.url

if __name__ == "__main__":
    try:
        opts , args = getopt.getopt(sys.argv[1:], "hl:vcn:d:x",
            ["help", 
            "language=",
            "verbose",
            "nocolor",
            "nick=",
            "desc="])
    except getopt.GetoptError:
        usage()
        sys.exit(1)

    ## Defaults
    verbose = False
    lang = "Plain Text"
    nick = "Unknown"
    desc = ""
    color = True
    stdin = 1
    for o,a in opts:
        if o == "-v":
            verbose=True
        if o in ("-h","--help"):
            usage()
            sys.exit()
        if o in ("-c","--nocolor"):
            color = False
        if o in ("-n" ,"--nick"):
            nick = a
        if o in ("-d" ,"--desc"):
            desc = a
        if o in ("-l","--language"):
            lang = a
        if o == "-x":
            stdin = 0
    if stdin: 
        try:
            text= sys.stdin.read()
        except KeyboardInterrupt:
            sys.exit(1)
    else: text= xclip()

    paster= Nopaste(text,verbose,lang,color,nick,desc)
    paster.params_encode()
    paster.paste()

