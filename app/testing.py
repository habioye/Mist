from mistcalendar import mistCalendar
import datetime
import mistcalendar
from datetime import date

# def headerstring():
#     calstring = "<!DOCTYPE html> "
#     calstring += "<html> "
#     calstring += "<head> "
#     calstring += "<head> "
#     calstring += "<title>Mist - Calendar View</title>"
#     calstring += " <meta name=\"viewport\""
#     calstring += " content=\"width=device-width, initial-scale=1\"> "
#     calstring += "<link rel=\"shortcut icon\" type=\"image/x-icon\" href=\"https://mist-asset.s3.us-east-2.amazonaws.com/temp+logo.ico\" /> "
#     calstring += "<link rel=\"stylesheet\" href= "
#     calstring += "\"https://cdn.jsdelivr.net/npm/bootstrap@4.6.0/dist/css/bootstrap.min.css\"> "
#     calstring += "</head> "
#     calstring += "<body>"
#     calstring += "<div>"
#     calstring += "<div class=\"col-9 grayborder\" id=\"eventinfo\"></div>"
#     calstring += "</div>"
#     calstring += "<div class =\"container-fluid\" style =\"background-color:rgb(255, 143, 0);\">"
#     calstring += "<div class=\"row\" style=\"background-color:rgb(255, 143, 0);\">"
#     calstring += "<div class = \"col-3\" display: inline-block; style = \"display:inline-block;padding:0;margin:0;\">"
#     calstring += "<a href = \"https://mist-princeton.herokuapp.com/\"><img src=\"https://mist-asset.s3.us-east-2.amazonaws.com/mist+map2.png\"  class=\"responsive\" style = \"max-width:30%;height:auto;float:left;\"></a>"
#     calstring += "</div>"
#     calstring += "<div class = \"col-6 align-middle\" display: inline-block;><center><h1 class=\"align-middle\" style=\"font-size:4vw;float:center;display:inline;\">Welcome to Mist!</h1></center></div>"
#     calstring += "<div class = \"col-3\"display: inline-block; style = \"display:inline-block;padding:0;\">"
#     calstring += "<a href = \"https://mist-princeton.herokuapp.com/calendar\"><img src=\"https://mist-asset.s3.us-east-2.amazonaws.com/mist+day.png\"  class=\"responsive\" style = \"max-width:30%;height:auto;float:right;\"></a>"
#     calstring += "</div>"
#     calstring += "</div>"
#     calstring += "</div>"
#     calstring += "<center><div class=\"header\">"
#     calstring += "<h2>Calendar View</h2>"
#     calstring += "<h3>Good <span id=\"ampmSpan\"></span> user.</h3>"
#     calstring += "</div></center>" 
#     return calstring       
    

# def ncalstringmaker(month, year):
#     currcal = mistcalendar.mistCalendar(month,year)
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

# def calstringmaker(month, year, currcal):
#    month = 5
#    year = 2021
#    currcal = mistcalendar.mistCalendar(month,year)
#    daycount = currcal.get_month_length()
#    firstday = currcal.get_first_day()
#    firstday = firstday % 7
#    firstday = firstday + 1

#    calstring = " <table class=\"table table-bordered table-hover\">"
#    calstring += "<tr style=\"background-color:black;color:white;\">"
#    calstring += "<th colspan=\"7\"><h3 align=\"center\">"
#    datetime_object = datetime.datetime.strptime(str(month), "%m")
#    month_name = datetime_object.strftime("%B")
#    calstring += month_name
#    calstring += " "
#    calstring += str(year)
#    calstring += "</h3></th>"
#    calstring += "</tr>"
#    calstring += "<tr style=\"background-color: rgb(110, 110, 110);\">"
#    calstring += "<th>Su</th>"
#    calstring += "<th>Mo</th>"
#    calstring += "<th>Tu</th>"
#    calstring += "<th>We</th>"
#    calstring += "<th>Th</th>"
#    calstring += "<th>Fr</th>"
#    calstring += "<th>Sa</th>"
#    calstring += "</tr>"
#    calstring += ""
#    currcount = -1 * firstday
#    currcount = currcount + 2
#    weekcount = 0
#    print(month)
#    print(year)
#    print(firstday)
#    print(currcount)
#    print(daycount)
#    for i in range(daycount + abs(currcount) + 1):
#       print(currcount)
#       if weekcount == 0:
#          calstring += "<tr>"
#       calstring += "<th>"
#       if currcount > 0:
#          calstring += str(currcount)
#       calstring += "</th>"
#       currcount+=1
#       if weekcount == 7:
#             calstring += "</tr>"
#             weekcount = 0
#    if weekcount != 0:
#       calstring += "</tr>"
#    calstring += "</table>"
#    print("")
#    print("somewhere")
#    return calstring
# def dateformat(year, month, day):
#     datestring = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
#     return datestring 

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

    calstring = "<div class=\"days\">"
    for i in range(padding + month_length):
        if i - padding < 0:
            calstring +="<div class=\"prev-date\" id = >"

            calstring += str(padding_to - (padding - i) + 1)
            calstring += "</div>"
        else:
            calstring += "<div class =\"days\" id = \"" + str(i+1) + "\" onclick = \"getPanelDetails(this.id)\">"
            if today.is_today((i + 1), month, year):
                calstring += "<div class=\"today\">"
                calstring += str(i + 1)
                calstring += "</div>"
            else:
                calstring += str(i + 1)
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
        calstring += str(j)
        calstring += "</div>"
    return calstring
 
def main():
   # print(mistdb.date_query("2021-03-01")[1][1])
   # print(dateformat(2001,5,3))
   # print("jank")
   # print(ncalstringmaker(11,2021))
   # print(calstringmaker(5,2021))
   today = mistcalendar.mistCalendar(12,2021)
   print(divcalstringmaker(today))
   # now = date.today()
   # print(now.month)
   
if __name__ == '__main__':
   main()