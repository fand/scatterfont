#! /usr/bin/env -S LD_LIBRARY_PATH=/home/gmork/.virtualenvs/27/lib/python2.7/ /home/gmork/.virtualenvs/27/bin/python
# -*- coding: utf-8 -*-

import sys
import random
import lxml.html
import cgi

# get font name
param = cgi.FieldStorage()
if param.has_key("name"):
    fontname = param["name"].value
else:
    fontname = "droidsans"

# open src file
with open("svg/" + fontname + ".svg", "r") as f:
    binary = f.read()

# process
d = lxml.html.fromstring(binary)

units = int(d.xpath("//font-face")[0].attrib["units-per-em"])
units_10 = units / 10
g_list = d.xpath("//glyph")
k_list = []
k_tmp = []

for g in g_list:

    if "d" in g.attrib:

        path = g.attrib["d"]

        
        # glitch vertex
        p_list = path.split("v")
        for i in range(1, len(p_list)):
            if random.random() < 0.3:
                p_list[i] = "v" + p_list[i]
            else:
                p_list[i] = "h" + p_list[i]

        path = "".join(p_list)

        
        # glitch curves
        p_list = path.split("q")
        for i in range(1, len(p_list)):
            if random.random() < 0.3:
                p_list[i] = ("q" +
                             str(random.randint(-units_10, units_10)) + " " +
                             str(random.randint(-units_10, units_10)) + " " +
                             str(random.randint(-units_10, units_10)) + " " +
                             str(random.randint(-units_10, units_10)) + " " +
                             "q" + p_list[i])
            else:
                p_list[i] = "q" + p_list[i]

        path = "".join(p_list)

        
        # add noises
        r = random.randint(0, 100)
        if r % 3 != 0:
            for i in range(r % 11):
                if r < 50:
                    path += ("v " + str(random.randint(-units, units)) +
                             "h " + str(random.randint(-units, units)))
                else:
                    path = ("v " + str(random.randint(-units, units)) +
                            "h " + str(random.randint(-units, units)) +
                            path)

        g.attrib["d"] = path


# output
s = lxml.html.tostring(d)
print "Content-type: image/svg+xml"
print ""
print s.encode('utf_8')
