#!/usr/bin/python
# This is a quick hack to take your old providers file and convert it
# to the new snppsend.ini format.  Make sure the old format providers
# file is in the current directory.  This app will merge the data into
# an existing snppsend.ini file in the current directory or create
# a new one.

import ConfigParser, os, sys, getopt

cfg = ConfigParser.RawConfigParser()
cfg.readfp(open("snppsend.ini","r"))
if not cfg.has_section("Providers"):
	cfg.add_section("Providers")

oldproviders = open("providers", "r")
for line in oldproviders:
	tmp = line.replace("\t\t", "\t").replace("\t\t", "\t").replace("\t\t", "\t").split("\t")
	cfg.set("Providers", tmp[0], tmp[1] + "," + tmp[2] + "," + tmp[3].strip())

cfg.write(open("snppsend.ini","w"))
