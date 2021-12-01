import mistcalender
import datetime

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
    

def ncalstringmaker(month, year):
    currcal = mistcalender.mistCalender(month,year)
    daycount = currcal.get_monthlength()
    firstday = currcal.get_first_day()
    firstday = firstday % 7
    firstday = firstday + 1
    
    calstring = headerstring()        
    calstring += "<table class=\"table table-bordered table-hover\">"
    calstring += "<tr style=\"background-color:black;color:white;\">"
    calstring += "<th colspan=\"7\"><h3 align=\"center\">"
    datetime_object = datetime.datetime.strptime(str(month), "%m")
    month_name = datetime_object.strftime("%B")
    calstring += month_name
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
    rangevalue = daycount + abs(currcount) + 1
    for i in range(rangevalue):
      if weekcount == 0:
         calstring += "<tr>"
      calstring += "<td>"
      if currcount > 0:
         calstring += str(currcount)
      calstring += "</td>"
      currcount+=1
      weekcount += 1
      if weekcount == 7:
         calstring += "</tr>"
         weekcount = 0
    if weekcount != 0:
      calstring += "</tr>"
    calstring += "</table>"
    calstring += "</body>"
    calstring += "</html>"
    return calstring

def calstringmaker(month, year):
   month = 5
   year = 2021
   currcal = mistcalender.mistCalender(month,year)
   daycount = currcal.get_monthlength()
   firstday = currcal.get_first_day()
   firstday = firstday % 7
   firstday = firstday + 1

   calstring = " <table class=\"table table-bordered table-hover\">"
   calstring += "<tr style=\"background-color:black;color:white;\">"
   calstring += "<th colspan=\"7\"><h3 align=\"center\">"
   datetime_object = datetime.datetime.strptime(str(month), "%m")
   month_name = datetime_object.strftime("%B")
   calstring += month_name
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
   currcount = -1 * firstday
   currcount = currcount + 2
   weekcount = 0
   print(month)
   print(year)
   print(firstday)
   print(currcount)
   print(daycount)
   for i in range(daycount + abs(currcount) + 1):
      print(currcount)
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
   print("")
   print("somewhere")
   return calstring
def dateformat(year, month, day):
    datestring = str(year).zfill(4) + "-" + str(month).zfill(2) + "-" + str(day).zfill(2)
    return datestring 

def main():
   print(dateformat(2001,5,3))
   print("jank")
   print(ncalstringmaker(11,2021))
   print(calstringmaker(5,2021))
   
if __name__ == '__main__':
   main()