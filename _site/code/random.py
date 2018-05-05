#!/usr/bin/env python
# Script to access random.org for random numbers
# Written by Ali Polatel
# Released under the Gnu General Public License v2
# XXX close stdout and open it as logfile in case of logfile is specified
# don't forget to remove coloring when writing to logfile ;)

import os
import sys
def checkversion():
    """ Check python version """
    too_old = "This program requires python v2.3 or greater\nYour python version :\n %s" % sys.version
    try:
        version = sys.version_info
        if (version[0] < 2) or (version[1] < 3):
            print too_old
            sys.exit(3)
    except AttributeError: # what if we don't have sys.version_info :P
        print too_old
        sys.exit(3)
checkversion()
import urllib
import urllib2
import optparse
import ConfigParser
import string
import re
import time
from optparse import OptionParser

home = os.environ['HOME']
CONF = {}

def main():
    """ Main function """
    opts = getopt()
    if not opts.verbose: switch(0)
    CONF["color"]=opts.color
    parser(opts.config) # Parse configuration
    if opts.file != "stdout":
        sys.stdout.close()
        cprint('cyan','o    Output redirected to %s ' % opts.file)
        if os.path.exists(opts.file):
            try: 
                cprint('green',' [appending]\n')
                sys.stdout = open(opts.file,"a")
            except:
                cprint('red',"o         Error opening output file : %s\n" % sys.exc_info()[1])
                sys.exit(1)
        else:
            sys.stdout = open(opts.file,"w")
    r = Random()
    if opts.mode=="checkbuf" and not opts.verbose: switch(1)
    while 1: # Loop until buffer is >=20%
        state=r.checkbuf()
        if state: break
        else: 
            switch(1)
            cprint('red',"Buffer level is less than 20%\n")
            cprint('red',"Sleeping for %d minutes before retrying\n" % CONF["wait"])
            cprint('red',"Hit ^C to exit\n")
            switch(0)
            try: time.sleep(CONF["wait"]*60)
            except KeyboardInterrupt: sys.exit(3)
    if   opts.mode == 'randnum':  print r.randnum()
    elif opts.mode == 'randseq':  print r.randseq()
    elif opts.mode == 'randbytes': print r.randbyte()
    sys.stdout.close()

def switch(state):
    """ Open/Close sys.stderr """
    if state:
        sys.stderr.close()
        sys.stderr = open("/dev/stderr","a+")
    else:
        sys.stderr.close()
        sys.stderr = open("/dev/null","a+")

def cprint(color,txt,bold=True):
    """ Colorize string 
    if shell is bash and if --nocolor is not set"""
    colors = {'bold': '\x1b[1m', 
              'normal':'\x1b[0m',
              'blue':'\x1b[34m',
              'green':'\x1b[32m',
              'red':'\x1b[31m',
              'cyan':'\x1b[36m'
             }
    if os.environ['SHELL'] != '/bin/bash' or not CONF["color"]: 
        sys.stdout.write(txt)
        return 0
    else:
        text = ""
        if bold: text += "%(bold)s" % colors
        for key in colors:
            if key == color: text += colors[key]
    text+=txt
    text+= "%(normal)s" % colors
    sys.stderr.write(text)
    return 0

def parser(config):
    """ Helper function to parse configurations """
    # look if ~/.randomrc exists and parse it
    # else write default configuration to ~/.randomrc
    if os.path.exists(config): 
        cprint('cyan',"o    Parsing configuration file %s\n" % config)
        parseconf(config)
    else: 
        switch(1)
        cprint('red',"o     Configuration file not found\n")
        cprint('red',"o     Writing default config to %s\n" % config)
        writeconf(config)
        cprint('red',"o     Adjust it as you want and rerun the script\n")
        sys.exit(2)

def writeconf(config):
    """ Write default configuration file """
#   print "%(bold)s%(red)s[warning]\t%(normal)s%(bold)sConfiguration file ~/.randomrc not found\n" % colors
#   print "%(bold)s\t\tWriting default configuration to ~/.randomrc\n" % colors
#   print "%(bold)s\t\tEdit it to suit your needs\n" % colors
    try:conf = open(config,"w")
    except:
        cprint('red',"o     Error opening config file : %s\n" % sys.exc_info()[1])
        sys.exit(1)
    conf.write(
"""# random.py configuration file\n# Have a look at http://random.org/http.html
[buffer]
wait= 3 # Minutes to wait if random.org buffer is <20%
[randnum]
num=100 # The number of integers wanted. Currently limited to 10,000. Defaults to 100.
min=1 # The lower bound of the interval (inclusive). This is the minimum value of any number returned by the server.
max=100 # The upper bound of the interval (inclusive). 
    # This is the maximum value of any number returned by the server. 
    # Currently restricted to 1,000,000,000 or less. Defaults to 100.
col=5   # The number of columns in which to format the numbers. Defaults to 5.
[randbyte]
nbytes=256 # Number of bytes to request
format=file # avaliable options are file,hex,octal and binary
[randseq]
min=1 # The smallest value in the sequence.
max=100 # The largest value in the sequence.    
""")
    conf.close()
    return 0

def parseconf(conffile):
    """ Parse configuration """
# TODO check for configuration file errors
    config = ConfigParser.ConfigParser()
    config.read(conffile)
    CONF["wait"]            = config.get("buffer","wait")
    CONF["num"]         = config.get("randnum","num")
    CONF["rnum_min"]        = config.get("randnum","min")
    CONF["rnum_max"]        = config.get("randnum","max")
    CONF["col"]         = config.get("randnum","col")
    CONF["nbytes"]      = config.get("randbyte","nbytes")
    CONF["format"]      = config.get("randbyte","format")
    CONF["rseq_min"]    = config.get("randseq","min")
    CONF["rseq_max"]    = config.get("randseq","max")
    # check for comments like format=file # <-- hey I'm here
    notint=('color','format') # int() all except those
    for key in CONF: 
        try: CONF[key] = re.sub(" ?#.*","",CONF[key])
        except TypeError: pass # CONF["color"] is boolean
        if key not in notint: CONF[key] = int(CONF[key])
    return 0

def getopt():
    """ Get options from command line"""
    name = "random.py"
    usage = "usage: %prog [options]"
    desc = "Get random numbers,sequences,bytes from http://random.org"
    modes = ["checkbuf","randnum","randseq","randbytes"]
    p = OptionParser(usage=usage,version="%prog 0.01",description=desc,prog=name)

    p.add_option("-v","--verbose",action="store_true",dest="verbose",default=False,help="be verbose")
    p.add_option("-C","--nocolor",action="store_false",dest="color",default=True,help="suppress coloring of output")
    p.add_option("-c","--config",default="%s/.randomrc" % home,metavar="FILE",dest="config",help="specify configuration file. [default:~/.randomrc]")
    p.add_option("-w","--write",default="stdout",metavar="FILE",dest="file",help="specify output FILE. [default:%default]")
    p.add_option("-m","--mode",default="randnum",dest="mode",help="Specify mode: checkbuf,randnum[default],randseq,randbytes")
    (opts,args) = p.parse_args()
    if opts.mode not in modes: p.error("Invalid mode")
    return opts

class Random:
    """ Main class including requests to scripts """
    def __init__(self):
        """ Initialize the class """
        self.url="http://www.random.org/cgi-bin"
        self.name = "random.py 0.01"
        self.mail = "polatel at gmail dot com" # E-mail to put in User-Agent
        self.headers = { "User-Agent" : "%s (%s)" % (self.name,self.mail) }

    def checkbuf(self):
        """ 
        Check random.org buffer 
        return 1 if buffer level is >20% and 0 otherwise 
        """
            cprint('cyan',"o    Checking random.org buffer\n")
            url = "%s/checkbuf" % self.url
        req = urllib2.Request(url,None,self.headers)
        handle = urllib2.urlopen(req)
        buf = handle.read()
        self.buffer = int ( buf.replace("%\n","") )
        cprint('cyan',"o    Buffer state : ")
        if self.buffer >= 20:
            cprint('green'," %d%%\n" % self.buffer)
            return 1
        else:
            cprint('red'," %d%%\n" % self.buffer)
            return 0

    def randnum(self):
        """
        Gets a list of integers from randnum script
        num : The number of integers wanted. Currently limited to 10,000. Defaults to 100.
        min : The lower bound of the interval (inclusive). 
              This is the minimum value of any number returned by the server. 
              Currently restricted to -1,000,000,000 or greater. 
              Defaults to 1.
        max : The upper bound of the interval (inclusive). 
              This is the maximum value of any number returned by the server. 
              Currently restricted to 1,000,000,000 or less. 
              Defaults to 100.
        col : The number of columns in which to format the numbers. Defaults to 5.
        """
        # XXX get these text messages out!
        txt='o  Requesting %(num)d integers from random.org [min:%(rnum_min)d,max:%(rnum_max)d,columns:%(col)d]\n'% CONF
        cprint('cyan',txt)
        url = "%s/randnum?num=%d&min=%d&max=%d&col=%d" % (self.url,CONF["num"],CONF["rnum_min"],CONF["rnum_max"],CONF["col"])
        req = urllib2.Request(url,None,self.headers)
        handle = urllib2.urlopen(req)
        return handle.read()

    def randbyte(self):
        """ 
        Gets a number of raw bytes from randbyte script 
        nbytes : The number of bytes requested. Currently restricted to 16,384. 
                 Defaults to 256.
        format : f -> the numbers are returned as a binary file of MIME type application/octet-stream.
                 h -> hexadecimal with MIME type text/plain
             o -> octal with MIME type text/plain
             b -> binary with MIME type text/plain
        """
            txt='o  Requesting %(nbytes)d raw bytes with format %(format)s from random.org\n'% CONF
        cprint('cyan',txt)
        url = "%s/randbyte?nbytes=%d&format=%s" % (self.url,CONF["nbytes"],CONF["format"][0])
        req = urllib2.Request(url,None,self.headers)
        handle = urllib2.urlopen(req)
        return handle.read()

    def randseq(self):
        """ 
        Gets a randomized sequence of numbers from randseq script
        min : The smallest value in the sequence
        max : The largest value in the sequence 
        """
        txt='o  Requesting a random sequence with intervals %(rseq_min)d:%(rseq_max)d.\n' % CONF
        cprint('cyan',txt)
        url = "%s/randseq?min=%d&max=%d" % (self.url,CONF["rseq_min"],CONF["rseq_max"])
        req = urllib2.Request(url,None,self.headers)
        handle = urllib2.urlopen(req)
        return handle.read()

if __name__ == "__main__":
    main()


