from apscheduler.scheduler import Scheduler


class Period(object):
    def __init__(self, name):
        self.name = name
    
    def getName(self):
        return self.name
        
    def createJob(self, scheduler, jobInfo, func):
        pass
        

class IntervalPeriod(Period):
    def __init__(self, name="", weeks=0,days=0, hours=0, minutes=0, seconds=0, start_date=None,
                 comment=None):
        super(IntervalPeriod, self).__init__(name)
        
        self.days = days                  # number of days to wait
        self.weeks = weeks                # number of weeks to wait
        self.hours = hours                # number of hours to wait
        self.minutes = minutes            # number of minutes to wait
        self.seconds = seconds            # number of seconds to wait
        self.start_date = start_date      # when to first execute 
        self.comment = comment            # comment
        
    def createJob(self, scheduler, jobInfo, func):
        return scheduler.add_interval_job(func, self.weeks, self.hours, self.minutes, self.seconds, self.start_date, [jobInfo])
    
        
    def __str__(self):
        ret = "IntervalPeriod(Name: " + self.name + ")"
        return ret    


class CronPeriod(Period):
    def __init__(self, name="", year="*", month="*", day="*", week="*",
                 day_of_week="*", hour="*", minute="*", second="0", start_date=None,
                 comment=None):
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
        
    def createJob(self, scheduler, jobInfo, func):
        return scheduler.add_cron_job(func, self.year, self.month, self.day, self.week, self.day_of_week, self.hour, self.minute, self.second,self.start_date, [jobInfo])
            
        
class DatePeriod(Period):
    def __init__(self, name, date, comment=None):
        super(DatePeriod, self).__init__(name)
        self.date = date
        self.comment = comment

    def __str__(self):
        ret = "DatePeriod(Name: " + self.name + ","+ str(self.date) + ")"
        return ret
        
    def createJob(self, scheduler, jobInfo, func):
        return scheduler.add_date_job(func, self.date, [jobInfo])





def parsePeriodList(periodlist,log):
    periods=[]
    log.i(periodlist)
    for name, values in periodlist.items():
        if "date" in values:
            periods.append(DatePeriod(name, **values))
            continue
        
        for i in [ "weeks","days", "hours", "minutes", "seconds", "start_date"]:
            if i in values:
                periods.append(IntervalPeriod(name, **values))
                continue
        
        for i in ["year", "month", "day", "week", "day_of_week", "hour", "minute", "second"]:
            if i in values:
                periods.append(CronPeriod(name, **values))
                continue
        
        log.w("ignoring Period: " +str(name))
        log.w("reason: could not determine PeriodType: " + str(values))
        
        
    return periods

