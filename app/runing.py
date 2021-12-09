from datetime import datetime
import mistcalender

print("what")
month = 12
year = 2021
currcal = mistcalender.mistCalender(12,2021)
daycount = currcal.get_month_length
firstday = currcal.get_first_day()
firstday = firstday % 7
firstday = firstday + 1

calstring = " <table class=\"table table-bordered table-hover\">"
calstring += "<tr style=\"background-color:black;color:white;\">"
calstring += "<th colspan=\"7\"><h3 align=\"center\">"
calstring += str(month)
calstring += " "
calstring += str(year)
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
    print("here")
    if weekcount == 0:
        calstring += "<tr>"
    calstring += "<th>"
    if currcount > 0:
        calstring += str(currcount)
    calstring += "</th>"
    currcount+=1
    if weekcount == 7:
        calstring += "</tr>"
        weekcount = 0
    if weekcount != 0:
        calstring += "</tr>"
    calstring += "</table>"
    
print("complete")