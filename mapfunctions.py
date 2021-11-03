#!/usr/bin/env python

#-----------------------------------------------------------------------
# mapfunctions.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import stderr
from flask import Flask, request, make_response
from flask import render_template
from mistdb import add_event_proto, map_query

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='.')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    long = request.args.get('Long')
    lat = request.args.get('Lat')
    text = request.args.get('Text')
    package = map_query("")
    if(package[0] == False)

    if long is not None:
        add_event_proto(long, lat, text)

    html = render_template("testmap.html", long = long, lat = lat, text = text)

    html = render_template(testmap.html, long = long, lat = lat, text = text)

    response = make_response(html)

    return response
