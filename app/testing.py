
import mistcalender
import datetime

def calstringmaker(month, year):
   currcal = mistcalender.mistCalender(month,year)
   daycount = currcal.monthlength
   firstday = currcal.get_first_day()
   firstday = firstday % 7
   firstday = firstday + 1
   print("the first day is")
   print(firstday)
   caldata = currcal.to_dict()
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
   calstring += ""
   calstring += ""
   currcount = -1 * firstday
   currcount = currcount + 2
   weekcount = 0
   while currcount <= daycount:
      if weekcount == 0:
         calstring += "<tr>"
      weekcount += 1
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
   
   return calstring

def main():
   print(calstringmaker(5,2021))
   
if __name__ == '__main__':
   main()