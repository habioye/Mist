#!/usr/bin/env python
#-----------------------------------------------------------------------
# calender.py
# Author: Hassan Abioye
#-----------------------------------------------------------------------
from datetime import date
from datetime import datetime
from calendar import monthrange
from sys import stderr

# this calender class initializes to the current day. When ever you want to 
# switch between months it always start you at the first day of each month. 
# No matter what day you have you should always be able to access information 
# about the month and the year. The data will be iso format.
class mistCalender:
    # months are represented [0:12]
    def __init__(self,month,year):
        today = date.today()
        # today.month something

        if month is None:
            self.month = today.month
        else:
            if month < 1 or month > 12:
                print("month is outside range", stderr)
                raise ValueError('month must be between 1 and 12')
            self.month = month
        self.day = today.day
        if year is None:
            self.year = today.year
        else:
            self.year = today.year

        
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.monthlength = monthrange(self.year, self.month)[1]


        
    
    def get_month(self):
        return self.month

    def get_day(self):
        return self.month
    
    def get_year(self):
        return self.year
    
    def get_first_day(self):
        return self.first_day
    
    
    def get_monthlength(self):
        return self.monthlength
    
    def next_month(self):
        self.month += 1
        self.month = self.month% 13
        if(self.month == 0):
            self.year += 1 
            self.month = 1
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.monthlength = monthrange(self.year, self.month)[1]
        return self.month
    
    def previous_month(self):
        self.month -= 1
        if(self.month == 0):
            self.year -= 1
            self.month = 0
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.monthlength = monthrange(self.year, self.month)[1]
        return self.month
        
    def next_year(self):
        self.year += 1
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.monthlength = monthrange(self.year, self.month)[1]
        return self.year
    
    def previous_year(self):
        self.year -= 1
        self.first_day = date(self.year,self.month,1).isoweekday()
        self.monthlength = monthrange(self.year, self.month)[1]
        return self.year
    
    def to_dict(self):
        return {'month': self.month, 'year': self.year, 'firstday': self.first_day, 'monthlength':self.monthlength}
    
#-----------------------------------------------------------------------

def _test():
    cal = mistCalender('None','None')
    print(cal.get_first_day)
    print("play")
    print(cal.get_day())
    
    print(cal.get_month())
    print(cal.get_year())
    cal.next_month()
    print(cal.get_month())
    cal.next_month()
    print(cal.get_month())
    print(cal.get_year())
    cal.previous_year()
    print(cal.get_year())
    

if __name__ == '__main__':
    _test()

