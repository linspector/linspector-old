"""

Copyright (c) 2011-2013 "Johannes Findeisen and Rafael Timmerberg"

This file is part of Linspector (http://linspector.org).

Linspector is free software: you can redistribute it and/or modify
it under the terms of the GNU Affero General Public License as
published by the Free Software Foundation, either version 3 of the
License, or (at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU Affero General Public License for more details.

You should have received a copy of the GNU Affero General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
"""


class Period(object):
    def __init__(self, name):
        self.name = name
    
    def get_name(self):
        return self.name
        
    def createJob(self, scheduler, jobInfo, func):
        pass
        

class IntervalPeriod(Period):
    def __init__(self, name="", weeks=0, days=0, hours=0, minutes=0, seconds=0, start_date=None, comment=None):
        super(IntervalPeriod, self).__init__(name)
        
        self.days = days                  # number of days to wait
        self.weeks = weeks                # number of weeks to wait
        self.hours = hours                # number of hours to wait
        self.minutes = minutes            # number of minutes to wait
        self.seconds = seconds            # number of seconds to wait
        self.start_date = start_date      # when to first execute 
        self.comment = comment            # comment
        
    def createJob(self, scheduler, jobInfo, func, **kwargs):
        start_date = self.start_date
        if kwargs["start_date"]:
            start_date = kwargs["start_date"]

        return scheduler.add_interval_job(func, weeks=self.weeks, hours=self.hours, minutes=self.minutes,
                                          seconds=self.seconds, start_date=start_date, args=[jobInfo])

    def __str__(self):
        ret = "IntervalPeriod(Name: " + self.name + ")"
        return ret    


class CronPeriod(Period):
    def __init__(self, name="", year="*", month="*", day="*", week="*", day_of_week="*", hour="*", minute="*",
                 second="0", start_date=None, comment=None):
        super(CronPeriod, self).__init__(name)
        self.year = year                # 4-digit year number
        self.month = month              # month number (1-12)
        self.day = day                  # day of the month (1-31)
        self.week = week                # ISO week number (1-53)
        self.day_of_week = day_of_week  # number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        self.hour = hour                # hour (0-23)
        self.minute = minute            # minute (0-59)
        self.second = second            # second (0-59)
        self.start_date = start_date
        self.comment = comment

    def __str__(self):
        ret = "CronPeriod(Name: " + self.name + ")"
        return ret
        
    def createJob(self, scheduler, jobInfo, func, **kwargs):
        start_date = self.start_date
        if kwargs["start_date"]:
            start_date = kwargs["start_date"]

        return scheduler.add_cron_job(func, year=self.year, month=self.month, day=self.day, week=self.week,
                                      day_of_week=self.day_of_week, hour=self.hour, minute=self.minute,
                                      second=self.second, start_date=start_date, args=[jobInfo])
            
        
class DatePeriod(Period):
    def __init__(self, name, date, comment=None):
        super(DatePeriod, self).__init__(name)
        self.date = date
        self.comment = comment

    def __str__(self):
        ret = "DatePeriod(Name: " + self.name + ", " + str(self.date) + ")"
        return ret
        
    def createJob(self, scheduler, jobInfo, func, **kwargs):
        try:
            return scheduler.add_date_job(func=func, date=self.date, args=[jobInfo])
        except Exception, e:
            return None