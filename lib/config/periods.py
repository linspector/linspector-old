class Period:
    def __init__(self, name="", year="*", month="*", day="*", week="*",
                 day_of_week=None, hour="*", minute="*", second="0",
                 comment=None):
        self.name = name
        self.year = year                # 4-digit year number
        self.month = month              # month number (1-12)
        self.day = day                  # day of the month (1-31)
        self.week = week                # ISO week number (1-53)
        self.day_of_week = day_of_week  # number or name of weekday (0-6 or mon,tue,wed,thu,fri,sat,sun)
        self.hour = hour                # hour (0-23)
        self.minute = minute            # minute (0-59)
        self.second = second            # second (0-59)
        self.comment = comment

    def __str__(self):
        ret = "Period(Name: " + self.name + " Year: " + self.year + " Month: " + self.month + ")"
        return ret


def parsePeriodList(periods):
    return [Period(name, **values) for name, values in periods.items()]

