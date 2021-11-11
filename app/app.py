#!/usr/bin/env python

#-----------------------------------------------------------------------
# mapfunctions.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import stderr
from flask import Flask, request, make_response
from flask import render_template
from json import dumps
from app import mistdb, templates

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    long = request.args.get('long')
    lat = request.args.get('lat')
    text = request.args.get('text')
    print(long)
    print(lat)
    print(text)
    if long is not None and lat is not None and text is not None:
        mistdb.add_event_proto(text, long, lat)
    package = mistdb.map_query("00:00:00-05:00", "23:59:59-05:00")
    if package[0] == False:
        print(package[1])
    else:
        print(package[1])
        # package = dumps(package[1])
        package = package[1]

    html = render_template("testmap.html", eventData = package)

    response = make_response(html)

    return response

@app.route('/calendar', methods=['GET'])
def calendar():
    package = mistdb.map_query("00:00:00-05:00", "23:59:59-05:00")
    if(package[0] == False):
        print(package[1])
    else:
        package = package[1]
    data = []

    for event in package:
        details = mistdb.details_query(event[0])
        if details[0]:
            data.push(details[1])
        else:
            print(details[2])

    html = render_template("calendar.html", eventData = data)
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get("PORT", 33507))

