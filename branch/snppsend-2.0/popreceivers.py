#!/usr/bin/python
# This is a quick hack to take your old receivers file and convert it
# to the new snppsend.conf format.

# cat old-receivers-file | popreceivers.py >> /etc/snppsend.conf

import ConfigParser, os, sys, getopt

cfg = ConfigParser.RawConfigParser()
cfg.add_section("Receivers")

oldreceivers = sys.stdin
for line in oldreceivers:
	tmp = line.replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").split("\t")
	cfg.set("Receivers", tmp[0], tmp[1] + "," + tmp[2].strip())

cfg.write(sys.stdout)
