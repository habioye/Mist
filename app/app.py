#!/usr/bin/env python

#-----------------------------------------------------------------------
# mapfunctions.py
# Author: Benjamin Nadon
#-----------------------------------------------------------------------

from sys import stderr
from flask import Flask, request, make_response
from flask import render_template
from app import mistdb, templates

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')


@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    long = request.args.get('long')
    lat = request.args.get('lat')
    text = request.args.get('text')
    package = map_query("00:00:00-05:00", "23:59:59-05:00")
    if(package[0] == False):
        print("error")

    if long is not None:
        add_event_proto(long, lat, text)

    html = render_template("testmap.html")

    response = make_response(html)

    return response

# if __name__ == "__main__":
#     app.debug = False
#     port = int(os.environ.get("PORT", 33507))
#
