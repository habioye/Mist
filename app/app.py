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

        html = render_template("testmap.html", eventData = points, userData = names, master = master)

        response = make_response(html)

        return response

@app.route('/inputpage', methods = ['GET'])
def input():
    username = authenticate()
    html = render_template("input.html")

    response = make_response(html)

    return response

@app.route('/details', methods = ['GET'])
def details():
    # username = authenticate()
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
    html = render_template('details.html', details = details, start = start, end = end)
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
    print("\n\n\n\n\n\nIs there going to be an end date? Let's find out!")
    print(endDate)
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
        print(package[1])
    friendslist = package[1]
    html = render_template('friendlist.html', friends = friendslist)
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

@app.route("/addfriend", methods = ['GET']){
    username = authenticate()
    netid = request.args.get('netid')
    print("add friendship " + str(username) + str(netid))
    mistdb.add_friendship(username, netid)
    mistdb.remove_friendrequest(username, netid)
    return redirect('/friendscreen')
}
@app.route("/removerequest", method = ['GET']){
username = authenticate()
netid = request.args.get('netid')
mistdb.remove_friendrequest(username, netid)
return redirect('/friendscreen')
}
@app.route("/removefriend", methods = ['GET'])
def removefriend():
    username = authenticate()
    netid = request.args.get('netid')
    print("remove friendship " + str(username) + str(netid))
    mistdb.remove_friendship(username, netid)
    return redirect('/friendscreen')


## creates the html document string to roughly create entire template.
def headerstring():
    calstring = "<!DOCTYPE html> "
    calstring += "<html> "
    calstring += "<head> "
    calstring += "<head> "
    calstring += "<title>Mist - Calendar View</title>"
    calstring += " <meta name=\"viewport\""
    calstring += " content=\"width=device-width, initial-scale=1\"> "
    calstring += "<link rel=\"shortcut icon\" type=\"image/x-icon\" href=\"https://mist-asset.s3.us-east-2.amazonaws.com/temp+logo.ico\" /> "
    calstring += "<link rel=\"stylesheet\" href= "
    calstring += "\"https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css\"> "
    calstring += "</head> "
    calstring += "<body>"
    calstring += "<div>"
    calstring += "<div class=\"col-9 grayborder\" id=\"eventinfo\"></div>"
    calstring += "</div>"
    calstring += "<div class =\"container-fluid\" style =\"background-color:rgb(255, 143, 0);\">"
    calstring += "<div class=\"row\" style=\"background-color:rgb(255, 143, 0);\">"
    calstring += "<div class = \"col-3\" display: inline-block; style = \"display:inline-block;padding:0;margin:0;\">"
    calstring += "<a href = \"https://mist-princeton.herokuapp.com/\"><img src=\"https://mist-asset.s3.us-east-2.amazonaws.com/mist+map2.png\"  class=\"responsive\" style = \"max-width:30%;height:auto;float:left;\"></a>"
    calstring += "</div>"
    calstring += "<div class = \"col-6 align-middle\" display: inline-block;><center><h1 class=\"align-middle\" style=\"font-size:4vw;float:center;display:inline;\">Welcome to Mist!</h1></center></div>"
    calstring += "<div class = \"col-3\"display: inline-block; style = \"display:inline-block;padding:0;\">"
    calstring += "<a href = \"https://mist-princeton.herokuapp.com/calendar\"><img src=\"https://mist-asset.s3.us-east-2.amazonaws.com/mist+day.png\"  class=\"responsive\" style = \"max-width:30%;height:auto;float:right;\"></a>"
    calstring += "</div>"
    calstring += "</div>"
    calstring += "</div>"
    calstring += "<center><div class=\"header\">"
    calstring += "<h2>Calendar View</h2>"
    calstring += "<h3>Good <span id=\"ampmSpan\"></span> user.</h3>"
    calstring += "</div></center>"
    return calstring

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

# creates an a calendar body based on using a table implementation.
# def altcalstring(currcal):
#     month = currcal.get_month()
#     year = currcal.get_year()
#     daycount = currcal.get_month_length()
#     firstday = currcal.get_first_day()
#     firstday = firstday % 7
#     firstday = firstday + 1
#     calstring = "<table class=\"table table-bordered table-hover\">"
#     calstring += "<tr style=\"background-color:black;color:white;\">"
#     calstring += "<th colspan=\"7\"><h3 align=\"center\">"
#     datetime_object = datetime.datetime.strptime(str(month), "%m")
#     month_name = datetime_object.strftime("%B")
#     calstring += month_name
#     calstring += " "
#     calstring += str(year)
#     calstring += "</h3></th>"
#     calstring += "</tr>"
#     calstring += "<tr style=\"background-color: rgb(110, 110, 110);\">"
#     calstring += "<th>Su</th>"
#     calstring += "<th>Mo</th>"
#     calstring += "<th>Tu</th>"
#     calstring += "<th>We</th>"
#     calstring += "<th>Th</th>"
#     calstring += "<th>Fr</th>"
#     calstring += "<th>Sa</th>"
#     calstring += "</tr>"
#     calstring += ""
#     calstring += ""
#     calstring += ""
#     currcount = -1 * firstday
#     currcount = currcount + 2
#     weekcount = 0
#     rangevalue = daycount + abs(currcount) + 1
#     for i in range(rangevalue):
#       if weekcount == 0:
#          calstring += "<tr>"
#       calstring += "<td>"
#       if currcount > 0:
#          calstring += str(currcount)
#         #  calstring += "\n"
#          date = dateformat(year, month, currcount)
#          events = mistdb.date_query(date)
#          # check if there is equal to false.
#          if events[0] is False:
#              calstring += "\n"
#              calstring += "A server error occurred. "
#              calstring += "Please contact the system administrator."
#          else:
#             for eventinformation in events[1]:
#                 calstring += "\n"
#                 calstring += "<a href = eventinfo?eventID="
#                 calstring += str(eventinformation[0]) + "&eventName="
#                 calstring += str(eventinformation[1]) + "&eventLocation="
#                 calstring += str(eventinformation[2]) + "&startTime="
#                 calstring += str(eventinformation[3]) + "&endTime="
#                 calstring += str(eventinformation[4]) + "\" target = \"_blank\">"
#                 calstring += str(eventinformation[1]) + "</a>"
#       calstring += "</td>"
#       currcount+=1
#       weekcount += 1
#       if weekcount == 7:
#          calstring += "</tr>"
#          weekcount = 0
#     if weekcount != 0:
#       calstring += "</tr>"
#     calstring += "</table>"



# creates a full calendar body based on using a table implementation
# def calstringmaker(currcal):
#     #currcal = mistcalendar.mistCalendar(month,year)
#     month = currcal.get_month()
#     year = currcal.get_year()
#     daycount = currcal.get_month_length()
#     firstday = currcal.get_first_day()
#     firstday = firstday % 7
#     firstday = firstday + 1
#     calstring = headerstring()
#     calstring += "<table class=\"table table-bordered table-hover\">"
#     calstring += "<tr style=\"background-color:black;color:white;\">"
#     calstring += "<th colspan=\"7\"><h3 align=\"center\">"
#     datetime_object = datetime.datetime.strptime(str(month), "%m")
#     month_name = datetime_object.strftime("%B")
#     calstring += month_name
#     calstring += " "
#     calstring += str(year)
#     calstring += "</h3></th>"
#     calstring += "</tr>"
#     calstring += "<tr style=\"background-color: rgb(110, 110, 110);\">"
#     calstring += "<th>Su</th>"
#     calstring += "<th>Mo</th>"
#     calstring += "<th>Tu</th>"
#     calstring += "<th>We</th>"
#     calstring += "<th>Th</th>"
#     calstring += "<th>Fr</th>"
#     calstring += "<th>Sa</th>"
#     calstring += "</tr>"
#     calstring += ""
#     calstring += ""
#     calstring += ""
#     currcount = -1 * firstday
#     currcount = currcount + 2
#     weekcount = 0
#     rangevalue = daycount + abs(currcount) + 1
#     for i in range(rangevalue):
#       if weekcount == 0:
#          calstring += "<tr>"
#       calstring += "<td>"
#       if currcount > 0:
#          calstring += str(currcount)
#         #  calstring += "\n"
#          date = dateformat(year, month, currcount)
#          events = mistdb.date_query(date)
#          # check if there is equal to false.
#          if events[0] is False:
#              calstring += "\n"
#              calstring += "A server error occurred. "
#              calstring += "Please contact the system administrator."
#          else:
#             for eventinformation in events[1]:
#                 calstring += "\n"
#                 calstring += "<a href = eventinfo?eventID="
#                 event_id = eventinformation[0]
#                 eventstuff = mistdb.details_query(event_id)
#                 if eventstuff[0]:
#                     calstring += "\n"
#                     calstring += "<a href = eventinfo?eventID="
#                     calstring += str(eventinformation[0]) + "&eventName="
#                     calstring += str(eventinformation[1]) + "&eventLocation="
#                     calstring += str(eventinformation[2]) + "&startTime="
#                     calstring += str(eventinformation[3]) + "&endTime="
#                     calstring += str(eventinformation[4]) + "\" target = \"_blank\">"
#                     calstring += str(eventinformation[1]) + "</a>"


#       calstring += "</td>"
#       currcount+=1
#       weekcount += 1
#       if weekcount == 7:
#          calstring += "</tr>"
#          weekcount = 0
#     if weekcount != 0:
#       calstring += "</tr>"
#     calstring += "</table>"
#     calstring += "</body>"
#     calstring += "</html>"
#     return calstring


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

@app.route('/calinfo', methods=['GET'])
def calinfo():
    month = request.args.get('month')
    year = request.args.get('year')
    if month is None and year is None:
        today = mistcalendar.mistCalendar("None", "None")
    elif month is None or year is None:
        print("ValueError: inconsistent input to calendar",file= stderr)
        html = render_template("error.html", error_type="Value Error", error_message="inconsistent input to calendar")
        response = make_response(html)
        return response
    else:
        today = mistcalendar.mistCalendar(month,year)



    # Decommisioned since we can assume that js will give us the right month and year combination.
    # dynamicnumber = request.args.get('dynamicstate')
    # if dynamicnumber is not None:
    #      if dynamicnumber == 1:
    #          today.previous_year()
    #      if dynamicnumber == 2:
    #          today.previous_month()
    #      if dynamicnumber == 3:
    #          today.next_month()
    #      if dynamicnumber == 4:
    #          today.next_year()



    #calstring = calstringmaker(today)
    # uses a div implementation for the calendar.





    #calstring = divcalstringmaker(today)
    calstring = "<p> calendar</p>"



    # while currcount <= daycount:
    #     if weekcount == 0:
    #         calstring += "<tr>"
    #     calstring += "<th>"
    #     if currcount > 0:
    #         calstring += str(currcount)
    #     calstring += "</th>"
    #     currcount+=1
    #     if weekcount == 7:
    #         calstring += "</tr>"
    #         weekcount = 0
    # if weekcount != 0:
    #     calstring += "</tr>"
    # calstring += "</table>"
    # print(calstring)
    #calstring = altcalstring(today)
    #html = render_template("calendar.html", calendarinfo=calstring)

    html = render_template(calstring)
    response = make_response(html)

    # response.set_cookie('month', today.get_month())
    # response.set_cookie('year', today.get_year())
    return response

def padding_from_first(first_day):
    padding = first_day % 6
    return padding

def padd_next(padding, length):
    next_padding = padding + length % 6
    return next_padding

def divcalstringmaker(today):
    padding_to = today.peek_previous_month_length()
    month_length = today.get_month_length()
    first_day = today.get_first_day()
    padding = padding_from_first(first_day)
    padding_next = padd_next(padding,month_length)
    year = today.get_year()
    month = today.get_month()

    calstring = "div class= \"container\""
    calstring += "<div class=\"calendar\">"
    calstring += "<div class=\"month\">"
    #calstring += "<i class=\"fas fa-angle-left prev\"></i>"
    calstring += "<div class=\"date\">"
    calstring += "<h1></h1>"
    calstring += "<p></p>"
    calstring += "</div>"
    #calstring += "<i class=\"fas fa-angle-right next\"></i>"
    calstring += "</div>"
    calstring += "<div class=\"weekdays\">"
    calstring += "<div>Sun</div>"
    calstring += "<div>Mon</div>"
    calstring += "<div>Tue</div>"
    calstring += "<div>Wed</div>"
    calstring += "<div>Wed</div>"
    calstring += "<div>Thu</div>"
    calstring += "<div>Fri</div>"
    calstring += "<div>Sat</div>"
    calstring += "</div>"
    calstring += "<div class=\"days\">"
    for i in range(padding + month_length):
        if i - padding < 0:
            calstring +="<div class=\"prev-date\" id = >"

            calstring += str(padding_to - (padding - i) + 1)
            calstring += "</div>"
        else:
            calstring += "<div class =\"days\" id = \"" + str(i+1) + "\" onclick = \"getPanelDetails(this.id)\">"
            if today.is_today(i + 1, month, year):
                calstring += "<div class=\"today\">"
                calstring += str(i + 1)
                calstring += "</div>"
            else:
                calstring += str(i + 1)
            date = dateformat(year, month, i+1)
            events = mistdb.date_query(date)
            # check if there is equal to false.
            if events[0] is False:
                calstring += "\n"
                calstring += "A server error occurred. "
                calstring += "Please contact the system administrator."
            else:
                for eventinformation in events[1]:
                    calstring += "\n"
                    calstring += "< div class=\"event\">"
                    calstring += "<a href = eventinfo?eventID="
                    event_id = eventinformation[0]
                    eventstuff = mistdb.details_query(event_id)
                    if eventstuff[0]:
                        calstring += "\n"
                        calstring += "<a href = eventinfo?eventID="
                        calstring += str(eventinformation[0]) + "&eventName="
                        calstring += str(eventinformation[1]) + "&eventLocation="
                        calstring += str(eventinformation[2]) + "&startTime="
                        calstring += str(eventinformation[3]) + "&endTime="
                        calstring += str(eventinformation[4]) + "\" target = \"_blank\">"
                        calstring += str(eventinformation[1]) + "</a>"
                    calstring += "</div>"
            calstring += "</div>"

    for j in range(padding_next):
        calstring += "<div class=\"next-date\">"
        calstring += str(i + 1)
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

    html = render_template("firsttimeuser.html", netid = netid)
    response = make_response(html)
    return response

if __name__ == "__main__":
    app.debug = False
    port = int(os.environ.get("PORT", 33507))
