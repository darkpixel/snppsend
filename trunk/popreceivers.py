#!/usr/bin/python
# This is a quick hack to take your old receivers file and convert it
# to the new snppsend.ini format.  Make sure the old format receivers
# file is in the current directory.  This app will merge the data into
# an existing snppsend.ini file in the current directory or create
# a new one.

import ConfigParser, os, sys, getopt

cfg = ConfigParser.RawConfigParser()
cfg.readfp(open("snppsend.ini","r"))
if not cfg.has_section("Receivers"):
	cfg.add_section("Receivers")

oldreceivers = open("receivers", "r")
for line in oldreceivers:
	tmp = line.replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").split("\t")
	cfg.set("Receivers", tmp[0], (tmp[1], tmp[2].strip()))

cfg.write(open("snppsend.ini","w"))
