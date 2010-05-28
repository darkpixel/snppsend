snppsend
--------

Copyright 2005-2010 Aaron C. de Bruyn

BSD Licensed

<insert BSD license here>  ;)


Note: This is *very* old code from when I first started dorking around
with python.

I'm planning to update Real Soon Now(tm) and add decent front-end.

-A


--WHAT IS SNPPSEND?--
snppsend is an application written in python to send messages to text (alpha-
numeric) pagers.  snppsend reads text from stdin, converts any combination
of CR/LF to a space and then sends the data to the recipients specified
on the command line.

--HELP AND SUPPORT--
snppsend runs perfectly on my various linux boxen.  Your mileage may vary.

If you experience any problems running snppsend on your machine, feel free to
drop me a message (aaron@heyaaron.com).

--INSTALL AND SETUP--
Installing snppsend is very easy.
 - Login as root.
 - Copy snppsend.py to /usr/local/bin
 - Copy snppsend.conf to /etc
 - Edit /etc/snppsend.conf with your favorite text editor

--ADVANCED USERS--
Anyone familiar with python can dive into the code and play.
Patches welcome.
