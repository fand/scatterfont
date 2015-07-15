#! /usr/bin/env python
# -*- coding: utf-8 -*-

from flask import Flask, request, session, g, redirect, url_for, render_template, Response
app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/favicon.ico')
def favicon():
    return redirect('/static/favicon.ico')

# @app.route('/<fontname>.svg')

@app.route('/<fontname>')
def font(fontname):
    fontdata = scatterFont(fontname)
    return Response(fontdata, status=200, mimetype='image/svg+xml')

import random
import lxml.html
import codecs

def scatterFont(fontname='droidsans'):

    # open src file
    filepath = "svg/" + fontname + ".svg"
    with codecs.open(filepath, "rb") as f:
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

    with codecs.open("./scattered.svg", "wb") as f:
        f.write(s)

    return s

if __name__ == '__main__':
    app.run(debug=True)
