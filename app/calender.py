#!/usr/bin/env python
#-----------------------------------------------------------------------
# calender.py
# Author: Hassan Abioye
#-----------------------------------------------------------------------
from datetime import date

# this calender class initializes to the current day. When ever you want to 
# switch between months it always start you at the first day of each month. 
# No matter what day you have you should always be able to access information 
# about the month and the year. The data will be iso format.
class Calender:
    # months are represented [0:12]
    def __init__(self):
        today = date.today
        # today.month something
        self.month = today.month
        self.day = today.day
        self.year = today.year
        self.first_day = date(self.year,self.month,1).isoweekday
        
    
    def get_month(self):
        return self.month

    def get_day(self):
        return self.month
    
    def get_year(self):
        return self.year
    
    def get_first_day(self):
        return self.first_day
    
        
    def next_month(self):
        self.month += 1
        self.month = self.month% 13
        if(self.month == 0):
            self.year += 1 
            self.month = 1

        self.first_day = date(self.year,self.month, 1)
        
        return self.month
    
    def previous_month(self):
        self.month -= 1
        if(self.month == 0):
            self.year -= 1
            self.month = 0
            
        self.first_day = date(self.year, self.month, 1)
        return self.month
    def next_year(self):
        self.year += 1
        return self.year
    
    def previous_year(self):
        self.year -= 1
        return self.year
#-----------------------------------------------------------------------

def _test():
    cal = Calender()

if __name__ == '__main__':
    _test()

