#!/usr/bin/env python

#---------------------------------------------------------------------
# mistdb.py
# Author: Anthony Gartner
#---------------------------------------------------------------------

from sys import stderr, exit
from contextlib import closing
from datetime import datetime, timezone, timedelta
import os
import re
import psycopg2
import hashlib

DATABASE_URL = os.environ['DATABASE_URL']

conn = psycopg2.connect(DATABASE_URL, sslmode='require')

#---------------------------------------------------------------------

def handle_plus (string):
    return re.sub(r'\W+', '', string)

#---------------------------------------------------------------------

# Functions for adding an event into the database. For the prototype,
# add_event_proto should be sufficient, as it adds based only on
# latitude and longitude coordinates. Other entry data is arbitrary.
# For a real event, the data input format MUST BE in the format
# specified, and dates and time MUST be in ISO format
# Two additional functions remove events, one by a given eventID, the
# other by specifying a time and date, and all events that have ended
# before that time are removed.

# Event adding function for the prototype. Takes string title, floating point
# x and y coords. Returns True on successful adding, False and Error Message
# on a fail

def add_event_proto(title, x_coord, y_coord):
    try:
        with conn:
            cursor = conn.cursor()
            print(title)
            print(x_coord)
            print(y_coord)

            with closing(conn.cursor()) as cursor:
                # Use a pairing algorithm and hashing to create an event ID
                event_id = str(int(hash(title)))
                # Create a the current date in EST and a one hour offset
                date_time = datetime.now(timezone(timedelta(hours=-5)))
                offset = date_time + timedelta(hours=1)
                coords = '(' + str(x_coord) + ', ' + str(y_coord) +')'

                stmt_str = '''INSERT INTO details (eventID, eventName, eventLocation,
                    startTime, endTime, eventDate, details, plannerID, coordinates,
                    roomNumber) VALUES (%s, %s, 'Princeton Campus', %s,
                    %s, %s, 'Sample Details', 'Example ID',
                    %s, 'Example Room');'''
                cursor.execute(stmt_str, (str(event_id),str(title),
                    str(date_time.time().isoformat()), str(offset.time().isoformat()),
                    str(date_time.date().isoformat()), str(coords)))

                return True
    except Exception as ex:
        error_msg = "A server error occurred in add_event_proto."
        error_msg +="Please contact the system administrator."
        print(ex, file = stderr, end=" ")
        print(error_msg, file = stderr)
        result = [False, error_msg]
        return result


# Real event adding function. Takes full suite of information as arguments,
# and hashes the coordinates into an eventID. Hashing might need to be changed
# to be more complex to ensure unique IDs, but seems statistically improbable.

def add_event(title, location, start, end, date, details, planner, x_coord, y_coord, number, endDate, privacy):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:
                print("Adding event")
                print(endDate)
                # Use the lower 8 bytes of sha256 hashing to create an event ID
                ei = hashlib.new('sha512_256')
                event_string = title + planner
                ei.update(event_string.encode('utf-8'))
                event_id = bytearray(ei.digest())[:4]
                event_id = int.from_bytes(bytes(event_id), 'big')
                print(event_id)

                stmt_str = '''INSERT INTO details (eventID, eventName, eventLocation,
                    startTime, endTime, eventDate, details, plannerID, coordinates,
                    roomNumber, endDate, eventPrivacy) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, '( %s , %s )'::point, %s, %s, %s)'''
                cursor.execute(stmt_str, (event_id, title, location, start,
                    end, date, details, planner, float(x_coord), float(y_coord), number, endDate, privacy))

                return True
    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Removes an event with the specified eventID. Returns True on success, and
# False and an error message on a failure

def remove_by_id(event_id):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM details
                                WHERE       eventID = %s'''

                cursor.execute(stmt_str, (event_id,))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Removes all events that have ended on the specified date after the specified time.
# Returns True on success, False and an error message on Failure. Probably good to be
# used for a nightly database cleanup.

def remove_by_datetime(date, time):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM details
                                WHERE       eventDate < %s
                                AND         endTime < %s'''

                cursor.execute(stmt_str, (date, time))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


#---------------------------------------------------------------------

# Database query functions. The first function should be used to get
# the initial events to populate the map with the currently occurring
# events. The secondary query will provide specifics about a particular
# event.

# Map populating query. Returns True and a list of all events in the
# given timeframe if successful. Returns False and an error message if
# unsuccessful. Times must be in ISO format and should be in EST.

def map_query(start, end):
    try:
        with conn:
            cursor = conn.cursor()
            print(start)
            print(end)

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  eventID,
                                        eventName,
                                        eventLocation,
                                        coordinates
                                FROM    details
                                WHERE   eventDate BETWEEN %s AND %s
                                ORDER BY    eventLocation,
                                            eventName'''
                cursor.execute(stmt_str, (start, end))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        error_msg +=" start: " + start + " end: " + end
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

#queries for only private friend events
def private_query(start, end, friendid):
    friendid = '%' + handle_plus(friendid) + '%'
    try:
        with conn:
            cursor = conn.cursor()


            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  eventID,
                                        eventName,
                                        eventLocation,
                                        coordinates
                                FROM    details
                                WHERE   (eventDate BETWEEN %s AND %s)
                                AND     eventPrivacy = 'PRIVATE'
                                AND     plannerID LIKE %s
                                ORDER BY    eventLocation,
                                            eventName'''
                cursor.execute(stmt_str, (start, end, friendid))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        error_msg +=" start: " + start + " end: " + end
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

def public_query(start, end):
    try:
        with conn:
            cursor = conn.cursor()
            print(start)
            print(end)

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  eventID,
                                        eventName,
                                        eventLocation,
                                        coordinates
                                FROM    details
                                WHERE   eventDate BETWEEN %s AND %s
                                AND     eventPrivacy = 'PUBLIC'
                                ORDER BY    eventLocation,
                                            eventName'''
                cursor.execute(stmt_str, (start, end))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        error_msg +=" start: " + start + " end: " + end
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result
# Queries the database for all a user's subscribed events to be displayed on the
# calendar. Returns True and a list of events on success, returns False and an
# error message on failure.

def cal_query(userID):
    userID = '%' + handle_plus(userID) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:
                stmt_str = '''  SELECT  eventID,
                                        eventName,
                                        eventLocation,
                                        startTime,
                                        endTime,
                                        eventDate
                                FROM    details
                                WHERE   details.eventID = participants.eventID
                                AND     participants.userID LIKE %s
                                ORDER BY    eventDate,
                                            startTime,
                                            eventName'''
                cursor.execute(stmt_str, (userID,))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

# Queries the database for all events on a given date. Returns True and a list of events on success,
# returns false and an error message on failure.
#
# To change it to show all events a user has subscribed to, uncomment lines 244 and 261 ,
# comment lines 245 and 260, and put the below AND statements beneath the WHERE statement
# AND   details.eventID = participants.eventID
# AND     participants.userID = %s
#def date_query(date, userID):
def date_query(date):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:
                stmt_str = '''  SELECT  eventID,
                                        eventName,
                                        eventLocation,
                                        startTime,
                                        endTime
                                FROM    details
                                WHERE   details.eventDate = %s
                                ORDER BY    startTime,
                                            eventName'''
                cursor.execute(stmt_str, (str(date),))
                # cursor.execute(stmt_str, (date, userID))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(date)
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

# Details query. Returns true and a list of event details in a list if successful.
# The indexes are in the order displayed in the google sheets about the database.
# If unsuccessful, returns False and an error message.

def details_query(event):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  *
                                FROM    details
                                WHERE   eventID = %s
                                ORDER BY    eventLocation,
                                            eventName'''

                cursor.execute(stmt_str, (str(event),))
                data = cursor.fetchall()

                if len(data) == 0:
                    error_msg = "No event with ID " + event + " exists"
                    return [False, error_msg]
                else:
                    return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


#---------------------------------------------------------------------

# User functions. A user must be added to the database the first time
# they log in. Until then, the other functions will not work. The userID
# should always be their netID/CAS authentification username.

# Add a user to the database. Returns true on a success, and False and
# an error message on a failure.

def add_user(netID, name):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''INSERT INTO userNames (userID, userName)
                    VALUES (%s, %s)'''

                cursor.execute(stmt_str, (netID, name))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Edit a user's name. Returns True on success, False on failure.

def edit_name(netID, name):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  UPDATE  userNames
                                SET     userName = %s
                                WHERE   userID = %s'''

                cursor.execute(stmt_str, (name, netID))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Add a friend relationship between two users. This function takes
# two people, and adds a row for both users as the userID, and the
# other user is the friend. Returns True on success and False and
# an error message on failure.

def add_friendship(user_a, user_b):
    if handle_plus(user_a) != handle_plus(user_b):
        try:
            with conn:
                cursor = conn.cursor()

                with closing(conn.cursor()) as cursor:

                    stmt_str = '''INSERT INTO friends (userID, friendID)
                        VALUES (%s, %s)'''

                    cursor.execute(stmt_str, (user_a, user_b))
                    cursor.execute(stmt_str, (user_b, user_a))

                    return True

        except Exception as ex:
            error_msg = "A server error occurred. "
            error_msg +="Please contact the system administrator."
            print(ex, file=stderr, end=" ")
            print(error_msg, file=stderr)
            result = [False, error_msg]
            return result

def add_friendrequest(requester, requestee):
    if handle_plus(requester) != handle_plus(requestee):
        try:
            with conn:
                cursor = conn.cursor()

                with closing(conn.cursor()) as cursor:

                    stmt_str = '''INSERT INTO requests (requester, requestee)
                        VALUES (%s, %s)'''

                    cursor.execute(stmt_str, (requester, requestee))

                    return True

        except Exception as ex:
            error_msg = "A server error occurred. "
            error_msg +="Please contact the system administrator."
            print(ex, file=stderr, end=" ")
            print(error_msg, file=stderr)
            result = [False, error_msg]
            return result

def remove_friendrequest(requester, requestee):
    requester = '%' + handle_plus(requester) + '%'
    requestee = '%' + handle_plus(requestee) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM requests
                                WHERE       requester LIKE %s
                                AND         requestee LIKE %s'''

                cursor.execute(stmt_str, (requester, requestee))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result
# Remove the friendship relationship between two users. Returns True
# if successful, false and error message if failure.

def remove_friendship(user_a, user_b):
    user_a = '%' + handle_plus(user_a) + '%'
    user_b = '%' + handle_plus(user_b) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM friends
                                WHERE       userID LIKE %s
                                AND         friendID LIKE %s'''

                cursor.execute(stmt_str, (user_a, user_b))
                cursor.execute(stmt_str, (user_b, user_a))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Queries the friends list and returns a list of friend netIDs and names
# as well as True if successful. Returns false and an error message if
# failure.

def friends_query(netID):
    netID = '%' + handle_plus(netID) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:
                # print("NET ID")
                # print(netID)
                stmt_str = '''  SELECT  friends.friendID
                                FROM    friends
                                WHERE   friends.userID LIKE %s
                                ORDER BY    friendID'''
                # stmt_str = '''  SELECT  friends.friendID,
                #                         userNames.userName
                #                 FROM    friends,
                #                         userNames
                #                 WHERE   friends.userID LIKE %s
                #                 AND     friends.friendID = userNames.userID
                #                 ORDER BY    userName'''
                cursor.execute(stmt_str, (netID,))
                data = cursor.fetchall()

                stmt_str = '''  SELECT  userName
                                FROM    userNames
                                WHERE   userID LIKE %s'''
                # print("FRIENDS LIST")
                # print(data)
                data = list(data)
                for i in range(len(data)):
                    data[i] = list(data[i])
                    id = '%' + handle_plus(data[i][0]) + '%'
                    cursor.execute(stmt_str, (id,))
                    name = cursor.fetchall()
                    # print(name)
                    data[i].append(name[0][0])
                # print("WITH NAMES")
                # print(data)
                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

def requests_query(netID):
    netID = '%' + handle_plus(netID) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:
                # print("NET ID")
                # print(netID)
                stmt_str = '''  SELECT  requests.requester
                                FROM    requests
                                WHERE   requests.requestee LIKE %s
                                ORDER BY    requester'''
                # stmt_str = '''  SELECT  friends.friendID,
                #                         userNames.userName
                #                 FROM    friends,
                #                         userNames
                #                 WHERE   friends.userID LIKE %s
                #                 AND     friends.friendID = userNames.userID
                #                 ORDER BY    userName'''
                cursor.execute(stmt_str, (netID,))
                data = cursor.fetchall()

                stmt_str = '''  SELECT  userName
                                FROM    userNames
                                WHERE   userID LIKE %s'''
                # print("FRIENDS LIST")
                # print(data)
                data = list(data)
                for i in range(len(data)):
                    data[i] = list(data[i])
                    id = '%' + handle_plus(data[i][0]) + '%'
                    cursor.execute(stmt_str, (id,))
                    name = cursor.fetchall()
                    data[i].append(name[0][0])
                # print("WITH NAMES")
                # print(data)
                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result
# Add a textual permission to a user. Returns True if successful, false
# and an error message if failure.

def add_permission(netID, perm):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''INSERT INTO permissions (userID, permissions)
                    VALUES (%s, %s)'''

                cursor.execute(stmt_str, (netID, perm))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Removes a permissions from a user. Returns True if successful, false
# and an error message if failure.

def remove_permission(netID, perm):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM permissions
                                WHERE       userID = %s
                                AND         permissions = %s'''

                cursor.execute(stmt_str, (netID, perm))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result



# Queries the permissions table and returns a list of permissions as well
# as True if successful. Returns false and an error message if failure.

def permissions_query(netID):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  permissions
                                FROM    permissions
                                WHERE   userID = %s
                                ORDER BY    permissions'''

                cursor.execute(stmt_str, (netID,))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Queries for the user's name, calls friends_query and permissions_query.
# Returns all user info and True on a success, returns False and an error
# message on failure. Catch all query to return all user info.

def user_query(netID):
    try:
        friends = friends_query(netID)
        if friends[0]:
            friends = friends[1]
        else:
            error_msg = "Error fetching friend data."
            return [False, error_msg]

        permissions = permissions_query(netID)
        if permissions[0]:
            permissions = permissions[1]
        else:
            error_msg = "Error fetching permission data."
            return [False, error_msg]

        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  userName
                                FROM    userNames
                                WHERE   userID = %s'''

                cursor.execute(stmt_str, (netID,))
                name = cursor.fetchall()

                return [True, name, friends, permissions]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result



#---------------------------------------------------------------------

# Three functions for adding, removing, and querying participants for
# events.

# Add a participant to a specified eventID. Return True on Success, False and error
# message on failure.

def add_participant(event_id, participant):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''INSERT INTO participants (eventID, userID)
                    VALUES (%s, %s)'''

                cursor.execute(stmt_str, (event_id, participant))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Remove a participant from a specified eventID. Return True on Success, False and error
# message on failure.

def remove_particpant(event_id, participant):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM participants
                                WHERE       eventID = %s
                                AND         userID = %s'''

                cursor.execute(stmt_str, (event_id, participant))
                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result

def search_query(search, netID ):
    netID = '%' + handle_plus(netID) + '%'
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  userID,
                                        userName
                                FROM    userNames
                                WHERE (userID LIKE %s
                                OR  LOWER(userName) LIKE LOWER(%s))
                                AND userID NOT IN (SELECT  friends.friendID
                                                FROM    friends
                                                WHERE   friends.userID LIKE %s) '''

                cursor.execute(stmt_str, (search, search, netID))
                names = cursor.fetchall()

                return [True, names]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Query the participants on a specified eventID, for a specified user.
# Return True and a list of participants that are the user's friends
# and their names on Success, False and error message on failure.

def particpants_query(event_id, netID):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  participants.userID,
                                        userNames.userName
                                FROM    participants,
                                        friends,
                                        userNames
                                WHERE   friends.userID = %s
                                AND     participants.eventID = %s
                                AND     friends.friendID = participants.userID
                                AND     participants.userID = userNames.userName
                                ORDER BY    userName'''

                cursor.execute(stmt_str, (netID, event_id))
                data = cursor.fetchall()

                return [True, data]

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


#---------------------------------------------------------------------

# Three functions for adding, removing, and querying tags for an event.

# Add a tag to a specified eventID. Return True on Success, False and error
# message on failure.

def add_tag(event_id, tag):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''INSERT INTO tags (eventID, tag)
                    VALUES (%s, %s)'''

                cursor.execute(stmt_str, (event_id, tag))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Remove a tag from a specified eventID. Return True on Success, False and error
# message on failure.

def remove_tag(event_id, tag):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  DELETE FROM tags
                                WHERE       eventID = %s
                                AND         tag = %s'''

                cursor.execute(stmt_str, (event_id, tag))

                return True

    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result


# Query the tags on a specified eventID. Return True and a list of tags on Success,
# False and error message on failure.

def tags_query(tag):
    try:
        with conn:
            cursor = conn.cursor()

            with closing(conn.cursor()) as cursor:

                stmt_str = '''  SELECT  tag
                                FROM    tags
                                WHERE   eventID = %s
                                ORDER BY    tag'''

                cursor.execute(stmt_str, (tag,))
                data = cursor.fetchall()

                return [True, data]


    except Exception as ex:
        error_msg = "A server error occurred. "
        error_msg +="Please contact the system administrator."
        print(ex, file=stderr, end=" ")
        print(error_msg, file=stderr)
        result = [False, error_msg]
        return result
