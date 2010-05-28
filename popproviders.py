#!/usr/bin/python
# This is a quick hack to take your old providers file and convert it
# to the new snppsend.conf format. 

# cat old-providers-file | popproviders.py >> /etc/snppsend.conf

import ConfigParser, os, sys, getopt

cfg = ConfigParser.RawConfigParser()
cfg.add_section("Providers")

oldproviders = sys.stdin
for line in oldproviders:
	tmp = line.replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").split("\t")
	cfg.set("Providers", tmp[0], tmp[1] + "," + tmp[2] + "," + tmp[3].strip())

cfg.write(sys.stdout)
