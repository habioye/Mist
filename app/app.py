#!/usr/bin/env python

#-----------------------------------------------------------------------
# mapfunctions.py
# Authors: Benjamin Nadon, Nick Cabrera, Anthony Gartner,
#          and Hassan Abioye
#-----------------------------------------------------------------------

from sys import stderr
from flask import Flask, request, make_response
from flask import render_template, session, abort
from json import dumps
# It seems this might break everything
# from calender import Calender
from werkzeug.utils import redirect
from app import mistdb, templates
from re import sub
from urllib.parse import quote
from urllib.request import urlopen
from app import mistcalender

#-----------------------------------------------------------------------

app = Flask(__name__, template_folder='templates')
app.secret_key = b',\xc0d\xdfj\x7f\x827u{\x15\xd3\x07\xe1O\x08'
CAS_URL = 'https://fed.princeton.edu/cas/'

#-----------------------------------------------------------------------
#-----------------------------------------------------------------------
# from PennyCas by Alex Halderman, Scott Karlin, Brian Kernighan,
# and Bob Dondero
# with small edits by Anthony Gartner

# Return url after stripping out the ticket parameter that was added
# by the CAS server

def strip_ticket(url):
    if url is None:
        return "No URL in Strip Ticket"
    url = sub(r'ticket=[^&]*&?', '', url)
    url = sub(r'\?&?$|&$', '', url)
    return url

# Validate a login ticket by contacting the CAS server. If valid, return
# the user's username; otherwise, return None

def validate(ticket):
    val_url = (CAS_URL + "validate" + '?service'
        + quote(strip_ticket(request.url)) + '&ticket=' +
        quote(ticket))
    lines = []
    with urlopen(val_url) as flo:
        lines = flo.readlines()
    if len(lines) != 2:
        return None
    first_line = lines[0].decode('utf-8')
    second_line = lines[1].decode('utf-8')
    if not first_line.startswith('yes'):
        return None
    return second_line

# Authenticate the remote user, and return the user's username. Do not
# return unless the user is successfully authenticated.

def authenticate():

    # If the username is in the session, then the user was authenticated
    # previously, return the username
    if 'username' in session:
        username = session.get('username')
        name = mistdb.user_query(username)
        if name[0]:
            if name[1][0] is None:
                abort(redirect('https://mist-princeton.herokuapp.com/firstimeuser'))
        return username

    # If the request does not contain a login ticket, then redirect the
    # browser to the login page to get one.
    ticket = request.args.get('ticket')
    if ticket is None:
        login_url = (CAS_URL + 'login?service='
            + quote(strip_ticket(request.url)))
        abort(redirect(login_url))

    # If the login ticket is invalid, then redirect the browser to the
    # login page to get a new one.
    username = validate(ticket)
    if username is None:
        login_url = (CAS_URL + 'login?service='
            + quote(strip_ticket(request.url)))
        abort(redirect(login_url))

    # The user is authenticated, so store the username in the session.
    session['username'] = username
    name = mistdb.user_query(username)
    if name[0]:
        if name[1][0] is None:
            abort(redirect('https://mist-princeton.herokuapp.com/firsttimeuser'))
    return username

@app.route('/logout', methods=['GET'])
def logout():
    authenticate()

    # Delete the user's username from the session
    session.pop('username')

    # Logout, and redirect the browser to the index page
    logout_url = (CAS_URL + 'logout?service='
        + quote(sub('logout', 'index', request.url)))
    abort(redirect(logout_url))
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():
    # username = authenticate()
    # long = request.args.get('long')
    # lat = request.args.get('lat')
    # text = request.args.get('text')
    # # print(long)
    # # print(lat)
    # # print(text)
    # if long is not None and lat is not None and text is not None:
    #     mistdb.add_event_proto(text, long, lat)
    package = mistdb.map_query("00:00:00-05:00", "23:59:59-05:00")
    # if package[0] == False:
        # print(package[1])
    # else:
        # print(package[1])
        # package = dumps(package[1])
    # There should be an exception thrown for the package data.
    package = package[1]

    html = render_template("testmap.html", eventData = package)

    response = make_response(html)

    return response

@app.route('/inputpage', methods = ['GET'])
def input():
    # username = authenticate()
    html = render_template("input.html")

    response = make_response(html)

    return response

@app.route('/addinput')
def addinput():
    # username = authenticate()
    loc = request.args.get('loc')
    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')
    date = request.args.get('date')
    coords = str(request.args.get('coords'))
    details = request.args.get('details')
    coords = coords.strip('{ }')
    coords = coords.split(',')
    x = coords[0].strip('"lat":')
    y = coords[1].strip("' '")
    y = y.strip(' "lng":')
    roomNum = request.args.get('roomnum')

    mistdb.add_event(title, loc, start, end, date, details, "netid", y, x, roomNum)
    return index()

@app.route('/friendscreen', methods = ['GET'])
def friendscreen():
    # username = authenticate()
    userid = 'getuserid'
    html = render_template('friendscreen.html', userid = userid)
    response = make_response(html)
    return response


def calstringmaker(month, year):

     currcal = mistcalender.mistCalender(month,year)
     daycount = currcal.monthlength
     firstday = currcal.get_first_day()
     firstday = firstday % 7
     firstday = firstday + 1
    
     caldata = currcal.to_dict()
     calstring = " <table class=\"table table-bordered table-hover\">"
     calstring += "<tr style=\"background-color:black;color:white;\">"
     calstring += "<th colspan=\"7\"><h3 align=\"center\">"
     calstring += month
     calstring += " "
     calstring += year
     calstring += "</h3></th>"
     calstring += "</tr>"
     calstring += "<tr style=\"background-color: rgb(110, 110, 110);\">"
     calstring += "<th>Su</th>"
     calstring += "<th>Mo</th>"
     calstring += "<th>Tu</th>"
     calstring += "<th>We</th>"
     calstring += "<th>Th</th>"
     calstring += "<th>Fr</th>"
     calstring += "<th>Sa</th>"
     calstring += "</tr>"
     calstring += ""
     calstring += ""
     calstring += ""
     currcount = -1 * firstday
     currcount = currcount + 2
     weekcount = 0
     while currcount <= daycount:
         if weekcount == 0:
            calstring += "<tr>"
         calstring += "<th>"
         if currcount > 0:
            calstring += currcount
         calstring += "</th>"
         currcount+=1
         if weekcount == 7:
             calstring += "</tr>"
             weekcount = 0
     if weekcount != 0:
        calstring += "</tr>"
     calstring += "</table>"
     
     return calstring


@app.route('/calendar', methods=['GET'])
def calendar():
    # username = authenticate()
    # package = mistdb.map_query("00:00:00-05:00", "23:59:59-05:00")
    # if(package[0] == False):
    #     print(package[1])
    # else:
    #     package = package[1]
    #
    data = []
    # for event in package:
    #     details = mistdb.details_query(event[0])
    #     if details[0]:
    #         data.push(details[1])
    #     else:
    #         print(details[1])

    # month = request.args.get('month')
    # year = request.args.get('year')
    # currcal = mistcalender.mistCalender(month,year)
    # daycount = currcal.monthlength
    # firstday = currcal.get_first_day()
    # firstday = firstday % 7
    # firstday = firstday + 1
    #
    #
    #
    # caldata = currcal.to_dict()
    # calstring = " <table class=\"table table-bordered table-hover\">"
    # calstring += "<tr style=\"background-color:black;color:white;\">"
    # calstring += "<th colspan=\"7\"><h3 align=\"center\">"
    # calstring += month
    # calstring += " "
    # calstring += year
    # calstring += "</h3></th>"
    # calstring += "</tr>"
    # calstring += "<tr style=\"background-color: rgb(110, 110, 110);\">"
    # calstring += "<th>Su</th>"
    # calstring += "<th>Mo</th>"
    # calstring += "<th>Tu</th>"
    # calstring += "<th>We</th>"
    # calstring += "<th>Th</th>"
    # calstring += "<th>Fr</th>"
    # calstring += "<th>Sa</th>"
    # calstring += "</tr>"
    # calstring += ""
    # calstring += ""
    # calstring += ""
    # currcount = -1 * firstday
    # currcount = currcount + 2
    # weekcount = 0
    # while currcount <= daycount:
    #
    #     if weekcount == 0:
    #         calstring += "<tr>"
    #     calstring += "<th>"
    #     if currcount > 0:
    #     calstring += currcount
    #     calstring += "</th>"
    #     currcount+=1
    #     if weekcount == 7:
    #         calstring += "</tr>"
    #         weekcount = 0
    #
    calstring = calstringmaker(12,2021)
    
    html = render_template("calendar.html", eventData = data)
    response = make_response(html)
    return response

@app.route('/firsttimeuser', methods=['GET'])
def firsttimeuser():
    netid = session.get('username')
    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    user_data = mistdb.user_query(netid)
    if user_data[0]:
        if user_data[1][0] is None and firstname is not None and lastname is not None:
            mistdb.add_user(netid, firstname + ' ' + lastname)
            abort(redirect('https://mist-princeton.herokuapp.com/'))

    html = render_template("firsttimeuser.html", netid = netid)
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get("PORT", 33507))
