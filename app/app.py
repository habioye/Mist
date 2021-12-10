#!/usr/bin/env python

#-----------------------------------------------------------------------
# mapfunctions.py
# Authors: Benjamin Nadon, Nick Cabrera, Anthony Gartner,
#          and Hassan Abioye
#-----------------------------------------------------------------------

from sys import stderr
from flask import Flask, request, make_response
from flask import render_template, session, abort
from flask import redirect as redir
from json import dumps
# It seems this might break everything
# from calendar import Calendar
from werkzeug.utils import redirect
from app import mistdb, templates
from re import sub
from urllib.parse import quote
from urllib.request import urlopen
from app import mistcalendar
import calendar
from datetime import date
import datetime


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
        return "something is badly wrong"
    url = sub(r'ticket=[^&]*&?', '', url)
    url = sub(r'\?&?$|&$', '', url)
    return url

# Validate a login ticket by contacting the CAS server. If valid, return
# the user's username; otherwise, return None

def validate(ticket):
    val_url = (CAS_URL + "validate"
        + '?service=' + quote(strip_ticket(request.url))
        + '&ticket=' + quote(ticket))
    lines = []
    with urlopen(val_url) as flo:
        lines = flo.readlines()   # Should return 2 lines.
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

    # If the username is in the session, then the user was
    # authenticated previously.  So return the username.
    if 'username' in session:
        username = session.get('username')
        name = mistdb.user_query(username)
        if name[0]:
            if len(name[1]) == 0:
                abort(redir('https://mist-princeton.herokuapp.com/firsttimeuser'))
        return username


    # If the request does not contain a login ticket, then redirect
    # the browser to the login page to get one.
    ticket = request.args.get('ticket')
    if ticket is None:
        login_url = (CAS_URL + 'login?service=' + quote(request.url))
        abort(redirect(login_url))

    # If the login ticket is invalid, then redirect the browser
    # to the login page to get a new one.
    username = validate(ticket)
    if username is None:
        login_url = (CAS_URL + 'login?service='
            + quote(strip_ticket(request.url)))
        abort(redirect(login_url))

    # The user is authenticated, so store the username in
    # the session.
    session['username'] = username
    name = mistdb.user_query(username)
    if name[0]:
        if len(name[1]) == 0:
            abort(redir('https://mist-princeton.herokuapp.com/firsttimeuser'))
    return username

@app.route('/logout', methods=['GET'])
def logout():
    authenticate()

    # Delete the user's username from the session
    session.pop('username')

    # Logout, and redirect the browser to the index page
    logout_url = (CAS_URL + 'logout?service='
        + quote(sub('logout', 'index', request.url)))
    abort(redir(logout_url))
#-----------------------------------------------------------------------
#-----------------------------------------------------------------------

@app.route('/', methods=['GET'])
@app.route('/index', methods=['GET'])
def index():

        username = authenticate()
        friendrequests = mistdb.requests_query(username)
        friendrequests = friendrequests[1]
        numrequests = len(friendrequests)




        startdate = request.args.get("start")
        enddate = request.args.get("end")
        option = request.args.get("option")

        if option is None or option == '':
            option = "all"

        if startdate is None or startdate == '':
            startdate = "-infinity"
        if enddate is None or enddate == '':
            enddate = "infinity"
        points = []
        if option == "friends":
            friendslist = mistdb.friends_query(username)
            friendslist = friendslist[1]
            print(friendslist)
            package = mistdb.private_query(startdate, enddate, username)
            package = package[1]
            print(package)
            points.extend(package)
            for friendID in friendslist:
                print(friendID[0])
                package = mistdb.private_query(startdate, enddate, friendID[0])
                print(package)
                package = package[1]
                points.extend(package)

        if option == "public":
            points = mistdb.public_query(startdate, enddate)
            points = points[1]

        if option == "all":
            package = mistdb.public_query(startdate, enddate)
            package = package[1]
            points.extend(package)


            package = mistdb.private_query(startdate, enddate, username)
            package = package[1]
            points.extend(package)

            friendslist = mistdb.friends_query(username)
            friendslist = friendslist[1]
            for friendID in friendslist:
                package = mistdb.private_query(startdate, enddate, friendID[0])
                package = package[1]
                points.extend(package)

    # if package[0] == False:
        # print(package[1])
    # else:
        # print(package[1])
        # package = dumps(package[1])
    # There should be an exception thrown for the package data.
        names = mistdb.user_query(username)
        names = names[1]
        master = mistdb.map_query(startdate,enddate)
        master = master[1]
        names.append(username)

        html = render_template("testmap.html", eventData = points, userData = names, num = numrequests, master = master)

        response = make_response(html)

        return response

@app.route('/inputpage', methods = ['GET'])
def input():
    username = authenticate()
    html = render_template("input.html", username = username)

    response = make_response(html)

    return response

@app.route('/details', methods = ['GET'])
def details():
    username = authenticate()
    eventid = request.args.get('eventid')
    # print(eventid)
    package = mistdb.details_query(str(eventid))
    if package[0] is False:
        print(package[1])
    details = package[1]
    start = str(details[0][3])
    start = start[:5]
    if(int(start[:2]) > 12):
        start = str(int(start[:2]) - 12) + start[2:] + ' PM'
    else:
        start = start + " AM"
    end = str(details[0][4])
    end = end[:5]
    if(int(end[:2]) > 12):
        end = str(int(end[:2]) - 12) + end[2:] + " PM"
    else:
        end = end + " AM"

    participants = mistdb.participants_query(eventid, username)
    if participants[0]:
        participants = participants[1]
        if len(participants) == 0:
            participants = None
    html = render_template('details.html', details = details, start = start, end = end, participants = participants)
    response = make_response(html)
    return response

@app.route('/addinput')
def addinput():
    username=authenticate()

    privacy = "PUBLIC"
    if(request.args.get('private') == 'on'):
        privacy = "PRIVATE"
        print(username + "created private event")
    username = authenticate()
    loc = request.args.get('loc')
    title = request.args.get('title')
    start = request.args.get('start')
    end = request.args.get('end')
    startDate = request.args.get('startDate')
    endDate = request.args.get('endDate')
    coords = str(request.args.get('coords'))
    details = request.args.get('details')
    coords = coords.strip('{ }')
    coords = coords.split(',')
    x = coords[0].strip('"lat":')
    y = coords[1].strip("' '")
    y = y.strip(' "lng":')
    roomNum = request.args.get('roomnum')

    mistdb.add_event(title, loc, start, end, startDate, details, username, y, x, roomNum, endDate, privacy)
    return redirect('/index')

@app.route('/friendscreen', methods = ['GET'])
def friendscreen():
    username = authenticate()
    username = username
    html = render_template('friendscreen.html', userid = username)
    response = make_response(html)
    return response

@app.route('/getfriends', methods = ['GET'])
def getfriends():
    #userid = request.args.get('search')
    userid = authenticate()
    package = mistdb.friends_query(userid)
    if package[0] is False:
        print("getfriends:")
        print(package[1])
    friendslist = package[1]
    print("getfriends")
    print(friendslist)
    html = render_template('friendlist.html', friends = friendslist)
    response = make_response(html)
    return response

@app.route('/getrequests', methods = ['GET'])
def getrequests():
    #userid = request.args.get('search')
    userid = authenticate()
    package = mistdb.requests_query(userid)
    if package[0] is False:
        print(package[1])
    friendslist = package[1]
    print("getrequests")
    print(friendslist)
    html = render_template('friendrequests.html', friends = friendslist)
    response = make_response(html)
    return response

@app.route('/getpending', methods = ['GET'])
def getpending():
    userid = authenticate()
    package = mistdb.pending_query(userid)
    if package[0] is False:
        print(package[1])
    friendslist = package[1]
    print("pending:")
    print(friendslist)
    html = render_template('pendingrequests.html', friends = friendslist)
    response = make_response(html)
    return response

@app.route('/searchfriends', methods = ['GET'])
def searchfriends():
    username = authenticate()
    search = request.args.get('search')
    if(str(search) == ''):
        friends = []
    else:
        search = '%' + str(search) + '%'
        package = mistdb.search_query(search, username)
        if package[0] is False:
            print(package[1])
        friends = package[1]
    html = render_template('friendsearch.html', friends = friends)
    response = make_response(html)
    return response

@app.route("/requestfriend", methods = ['GET'])
def requestfriend():
    username = authenticate()
    netid = request.args.get('netid')
    print("request friendship " + str(username) + str(netid))
    mistdb.add_friendrequest(username, netid)
    return redirect('/friendscreen')

@app.route("/addfriend", methods = ['GET'])
def addfriend():
    username = authenticate()
    netid = request.args.get('netid')
    print("add friendship " + str(username) + str(netid))
    mistdb.add_friendship(username, netid)
    mistdb.remove_friendrequest(netid, username)
    return redirect('/friendscreen')

@app.route("/removerequest", methods = ['GET'])
def removerequest():
    username = authenticate()
    netid = request.args.get('netid')
    mistdb.remove_friendrequest(netid, username)
    mistdb.remove_friendrequest(username, netid)

    return redirect('/friendscreen')

@app.route("/cancelrequest", methods = ['GET'])
def cancelrequest():
    username = authenticate()
    netid = request.args.get('netid')
    mistdb.remove_friendrequest(username, netid)
    return redirect('/friendscreen')

@app.route("/removefriend", methods = ['GET'])
def removefriend():
    username = authenticate()
    netid = request.args.get('netid')
    print("remove friendship " + str(username) + str(netid))
    mistdb.remove_friendship(username, netid)
    return redirect('/friendscreen')




def dateformat(year, month, day):
    datestring = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
    return datestring


# gives event info when you click a link to an event.
@app.route('/eventinfo', methods = ['GET'])
def eventinfo():
    eventID = request.args.get('eventID')
    eventName = request.args.get('eventName')
    eventLocation = request.args.get('eventLocation')
    startTime = request.args.get('startTime')
    endTime = request.args.get('endTime')


    html = render_template('eventinfo.html', eventID = eventID, eventName = eventName, eventLocation = eventLocation, startTime = startTime, endTime = endTime)
    response = make_response(html)
    return response
    # check when there is no such eventinfo



@app.route('/calendar', methods=['GET'])
def calendar():
    username = authenticate()
    # package = mistdb.map_query("00:00:00-05:00", "23:59:59-05:00")
    # if(package[0] == False):
    #     print(package[1])
    # else:
    #     package = package[1]
    #
    #data = []
    # for event in package:
    #     details = mistdb.details_query(event[0])
    #     if details[0]:
    #         data.push(details[1])
    #     else:
    #         print(details[1])


    html = render_template("calendar.html")

    response = make_response(html)

    return response

def month_full(month):
    months = ["Unknown",
          "January",
          "Febuary",
          "March",
          "April",
          "May",
          "June",
          "July",
          "August",
          "September",
          "October",
          "November",
          "December"]
    name = months[month]
    return name

@app.route('/calinfo', methods=['GET'])
def calinfo():
    month = request.args.get('month')
    year = request.args.get('year')
    if month is None and year is None:
        today = mistcalendar.mistCalendar("None", "None")
    else:
        today = mistcalendar.mistCalendar(month,year)





    calstring = divcalstringmaker(today)
  
    month_name = month_full(int(month))

    html = render_template("calform.html",month = month_name, year = year,days= calstring)
    response = make_response(html)
    return response

def padding_from_first(first_day):
    padding = first_day % 6
    return padding

def padd_next(padding, length):
    next_padding = 7 - ((padding + length) % 7)
    return next_padding

def divcalstringmaker(today):
    padding_to = today.peek_previous_month_length()
    month_length = today.get_month_length()
    first_day = today.get_first_day()
    padding = padding_from_first(first_day)
    padding_next = padd_next(padding,month_length)
    year = today.get_year()
    month = today.get_month()

    calstring = "<div class=\"days\">"
    for i in range(padding + month_length):
        if i - padding < 0:
            calstring +="<div class=\"prev-date\" id = >"

            calstring += str(padding_to - (padding - i) + 1)
            calstring += "</div>"
        else:
            calc_day = i+1-padding
            calstring += "<div class =\"days\" id = \"" + str(calc_day) + "\" onclick = \"getPanelDetails(this.id)\">"
            if today.is_today(calc_day, month, year):
                calstring += "<div class=\"today\">"
                calstring += str(calc_day)
                calstring += "</div>"
            else:
                calstring += str(calc_day)
            # date = dateformat(year, month, i+1)
            # events = mistdb.date_query(date)
            # # check if there is equal to false.
            # if events[0] is False:
            #     calstring += "\n"
            #     calstring += "A server error occurred. "
            #     calstring += "Please contact the system administrator."
            # else:
            #     for eventinformation in events[1]:
            #         calstring += "\n"
            #         calstring += "< div class=\"event\">"
            #         calstring += "<a href = eventinfo?eventID="
            #         event_id = eventinformation[0]
            #         eventstuff = mistdb.details_query(event_id)
            #         if eventstuff[0]:
            #             calstring += "\n"
            #             calstring += "<a href = eventinfo?eventID="
            #             calstring += str(eventinformation[0]) + "&eventName="
            #             calstring += str(eventinformation[1]) + "&eventLocation="
            #             calstring += str(eventinformation[2]) + "&startTime="
            #             calstring += str(eventinformation[3]) + "&endTime="
            #             calstring += str(eventinformation[4]) + "\" target = \"_blank\">"
            #             calstring += str(eventinformation[1]) + "</a>"
            #         calstring += "</div>"
            calstring += "</div>"

    for j in range(padding_next):
        calstring += "<div class=\"next-date\">"
        calstring += str(j+1)
        calstring += "</div>"
    return calstring


@app.route('/caldayinfo', methods=['GET'])
def caldayinfo():
    eventstring = "<p> events</p>"
    # day = int(request.args.get('day'))
    # month = int(request.args.get('month'))
    # year = int(request.args.get('year'))
    # date = dateformat(year, month, day)
    # events = mistdb.date_query(date)
    # eventstring = "<div>"
    # if events[0] is False:
    #     eventstring += "\n"
    #     eventstring += "A server error occurred. "
    #     eventstring += "Please contact the system administrator."
    #     eventstring += "</div>"
    #     return eventstring
    # else:
    #     for eventinformation in events[1]:
    #         eventstring += "\n"
    #         eventstring += "<a href = eventinfo?eventID="
    #         eventstring += str(eventinformation[0]) + "&eventName="
    #         eventstring += str(eventinformation[1]) + "&eventLocation="
    #         eventstring += str(eventinformation[2]) + "&startTime="
    #         eventstring += str(eventinformation[3]) + "&endTime="
    #         eventstring += str(eventinformation[4]) + "\" target = \"_blank\">"
    #         eventstring += str(eventinformation[1]) + "</a>"
    # eventstring += "</div>"
    return eventstring








@app.route('/signup', methods=['GET'])
def signup():
    username = authenticate()
    eventID = request.args.get('eventid')
    print("EVENT ID!")
    print(eventID)
    mistdb.add_participant(eventID, username)

    return redirect('/index')


@app.route('/firsttimeuser', methods=['GET'])
def firsttimeuser():
    netid = session.get('username')

    firstname = request.args.get('firstname')
    lastname = request.args.get('lastname')
    user_data = mistdb.user_query(netid)
    if user_data[0]:
        if len(user_data[1]) == 0 and firstname is not None and lastname is not None:
            mistdb.add_user(netid, firstname + ' ' + lastname)
            abort(redir('https://mist-princeton.herokuapp.com/'))
        elif firstname is not None and lastname is not None:
            mistdb.edit_name(netid, firstname + ' ' + lastname)
            abort(redir('https://mist-princeton.herokuapp.com/'))



    html = render_template("firsttimeuser.html", netid = netid)
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get("PORT", 33507))
