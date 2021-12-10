from mistcalendar import mistCalendar
import datetime
import mistcalendar
from datetime import date
from sys import stderr


# def month_full(month):
#     months = ["Unknown",
#           "January",
#           "Febuary",
#           "March",
#           "April",
#           "May",
#           "June",
#           "July",
#           "August",
#           "September",
#           "October",
#           "November",
#           "December"]
#     name = months[month]
#     return name


# def calinfo(month,year):

#     if month is None and year is None:
#         today = mistcalendar.mistCalendar("None", "None")


#     else:
#         today = mistcalendar.mistCalendar(month,year)



#     # Decommisioned since we can assume that js will give us the right month and year combination.
#     # dynamicnumber = request.args.get('dynamicstate')
#     # if dynamicnumber is not None:
#     #      if dynamicnumber == 1:
#     #          today.previous_year()
#     #      if dynamicnumber == 2:
#     #          today.previous_month()
#     #      if dynamicnumber == 3:
#     #          today.next_month()
#     #      if dynamicnumber == 4:
#     #          today.next_year()



#     #calstring = calstringmaker(today)
#     # uses a div implementation for the calendar.




#     calstring = divcalstringmaker(today)
#     #calstring = "<p> calendar</p>"



#     # while currcount <= daycount:
#     #     if weekcount == 0:
#     #         calstring += "<tr>"
#     #     calstring += "<th>"
#     #     if currcount > 0:
#     #         calstring += str(currcount)
#     #     calstring += "</th>"
#     #     currcount+=1
#     #     if weekcount == 7:
#     #         calstring += "</tr>"
#     #         weekcount = 0
#     # if weekcount != 0:
#     #     calstring += "</tr>"
#     # calstring += "</table>"
#     # print(calstring)
#     #calstring = altcalstring(today)
#     #html = render_template("calendar.html", calendarinfo=calstring)
#     month_name = month_full(month)


#     # response.set_cookie('month', today.get_month())
#     # response.set_cookie('year', today.get_year())
#     return month_name

# def padding_from_first(first_day):
#     padding = first_day % 6
#     return padding

# def padd_next(padding, length):
#     next_padding = padding + length % 6
#     return next_padding

# def divcalstringmaker(today):
#     padding_to = today.peek_previous_month_length()
#     month_length = today.get_month_length()
#     first_day = today.get_first_day()
#     padding = padding_from_first(first_day)
#     padding_next = padd_next(padding,month_length)
#     year = today.get_year()
#     month = today.get_month()

#     calstring = "<div class=\"days\">"
#     for i in range(padding + month_length):
#         if i - padding < 0:
#             calstring +="<div class=\"prev-date\" id = >"

#             calstring += str(padding_to - (padding - i) + 1)
#             calstring += "</div>"
#         else:
#             calstring += "<div class =\"days\" id = \"" + str(i+1-padding) + "\" onclick = \"getPanelDetails(this.id)\">"
#             if today.is_today(i + 1, month, year):
#                 calstring += "<div class=\"today\">"
#                 calstring += str(i + 1 - padding)
#                 calstring += "</div>"
#             else:
#                 calstring += str(i + 1 - padding)
#             # date = dateformat(year, month, i+1)
#             # events = mistdb.date_query(date)
#             # # check if there is equal to false.
#             # if events[0] is False:
#             #     calstring += "\n"
#             #     calstring += "A server error occurred. "
#             #     calstring += "Please contact the system administrator."
#             # else:
#             #     for eventinformation in events[1]:
#             #         calstring += "\n"
#             #         calstring += "< div class=\"event\">"
#             #         calstring += "<a href = eventinfo?eventID="
#             #         event_id = eventinformation[0]
#             #         eventstuff = mistdb.details_query(event_id)
#             #         if eventstuff[0]:
#             #             calstring += "\n"
#             #             calstring += "<a href = eventinfo?eventID="
#             #             calstring += str(eventinformation[0]) + "&eventName="
#             #             calstring += str(eventinformation[1]) + "&eventLocation="
#             #             calstring += str(eventinformation[2]) + "&startTime="
#             #             calstring += str(eventinformation[3]) + "&endTime="
#             #             calstring += str(eventinformation[4]) + "\" target = \"_blank\">"
#             #             calstring += str(eventinformation[1]) + "</a>"
#             #         calstring += "</div>"
#             calstring += "</div>"

#     for j in range(padding_next):
#         calstring += "<div class=\"next-date\">"
#         calstring += str(j+1)
#         calstring += "</div>"
#     return calstring





def main():
    # print(mistdb.date_query("2021-03-01")[1][1])
    # print(dateformat(2001,5,3))
    # print("jank")
    # print(ncalstringmaker(11,2021))
    # print(calstringmaker(5,2021))
    hello = mistcalendar.mistCalendar(1,2022)
    print(hello.peek_previous_month_length())
    print(hello.get_month_length())
    print(hello.get_first_day())

    # now = date.today()
    # print(now.month)
   
if __name__ == '__main__':
   main()