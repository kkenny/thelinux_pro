#!/usr/bin/python
# Procmail filter to scan mails with clamav
# Clamd should be running for this to work
# Written by Ali Polatel
# Released under the GNU General Public License v2
################################################################################
# The following recipe show how you might use this code with procmail          #
#                                                                              #
#   :0fw: virus1.lock                                                          #
#   |/path/to/clamdfilter.py                                                   #
#                                                                              #
#                                                                              #
# This recipe marks the email with the X-CLAMAV field if a virus is            #
# found.                                                                       #
################################################################################


import os
import socket
import sys
import random
import re
import email


client = socket.socket(socket.AF_UNIX,socket.SOCK_STREAM)
client.connect("/var/run/clamav/clamd.sock")

text = sys.stdin.read()
mail = email.message_from_string(text)
name = '/tmp/clammail%.3f' % random.random()
temp = open(name,'w')
temp.write(text)
temp.close()
os.chmod(temp.name,0777)
client.send('SCAN %s\n\n' % temp.name)

while True:
        try:    
                data =client.recv(1024)
                if not data:break
		else: ret = data
        except KeyboardInterrupt:break
os.remove(name)
client.close()
p = re.search (r'\s[^/].*',ret)
del mail['X-ClamAV']
mail.add_header('X-ClamAV',p.group())
print mail.as_string()

