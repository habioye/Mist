#!/usr/bin/env python
#-----------------------------------------------------------------------
# calendar.py
# Author: Hassan Abioye
#-----------------------------------------------------------------------
from datetime import date
from datetime import datetime
from calendar import monthrange
from sys import stderr



# this calendar class initializes to the current day. When ever you want to
# switch between months it always start you at the first day of each month.
# No matter what day you have you should always be able to access information
# about the month and the year. The data will be iso format. This implies that date information will not start at 0 for days or months. This also implies that years will not have a year 0.
class mistCalendar:
    # months are represented from 1 to 12
    def __init__(self,month,year):
        try: 
            today = date.today()
            # today.month something

            if month == "None" or year == "None":
                self.month = today.month
                self.year = today.year
                self.day = today.day
            else:
                self.month = int(month)
                self.year = int(year)
                self.day = today.day

            if self.month < 1 or self.month > 12:
                raise ValueError("month must be between 1 and 12")

            
            if self.year < 1:
                raise ValueError("year must be greater than or equal to 1")

            self.first_day = date(self.year,self.month,1).isoweekday()
            self.month_length = monthrange(self.year, self.month)[1]
        except ValueError as ex:
            print(ex)
            
            

    def is_today(day, month, year):
        today = date.today()
        if day == today.day and month == today.month and year == today.year:
            return True
        else:
            return False

    def peek_previous_month_length(self):
        curr_month = self.month
        curr_year = self.year
        curr_month -= 1
        if(curr_month == 0):
            curr_year -= 1
            curr_month = 12
        month_length = monthrange(curr_year,curr_month)[1]
        return month_length
        
    def get_first_day(self):
        return self.first_day
        
    def get_day(self):
        return self.day
        
    def get_month(self):
        return self.month

    def get_month_length(self):
        return self.month_length

    def get_year(self):
        return self.year

    def __update(self):
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.month_length = monthrange(self.year, self.month)[1]

    def next_month(self):
        self.month += 1
        self.month = self.month% 13
        if(self.month == 0):
            self.year += 1
            self.month = 1
        self.__update()
        return self.month

    def previous_month(self):
        self.month -= 1
        if(self.month == 0):
            self.year -= 1
            self.month = 12
        self.__update()
        return self.month

    def next_year(self):
        self.year += 1
        self.__update()
        return self.year

    def previous_year(self):
        self.year -= 1
        self.__update()
        return self.year
    
    

    def to_dict(self):
        return {'month': self.month, 'year': self.year, 'firstday': self.first_day, 'month_length':self.month_length}

#-----------------------------------------------------------------------

def _test():
    #null calendar
    cal_None = mistCalendar("None","None")
    
    # testing info about calendar
    cal = mistCalendar(12,2021)
    print(cal.peek_previous_month_length())
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())
    print(cal.get_day())
    
    
    print("month switching")
    cal.next_month()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.next_month()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.previous_month()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.previous_month()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    print("year switching")
    cal.previous_year()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.next_year()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.next_year()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())

    cal.previous_year()
    print(cal.get_month())
    print(cal.get_year())
    print(cal.get_first_day())
    
    print("testing firstday")
    firstcal = mistCalendar(8,2021)
    print(firstcal.get_first_day())
    secondcal = mistCalendar(5,2021)
    print(secondcal.get_first_day())


if __name__ == '__main__':
    _test()
