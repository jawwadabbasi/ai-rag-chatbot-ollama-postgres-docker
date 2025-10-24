from datetime import datetime, timezone

class Common:

    def Date():

        return datetime.now(timezone.utc).strftime('%Y-%m-%d')

    def Datetime():

        return datetime.now(timezone.utc).strftime('%Y-%m-%d %H:%M:%S')

    def DateObject():

        return datetime.strptime(Common.Date(), '%Y-%m-%d')

    def DatetimeObject():

        return datetime.strptime(Common.Datetime(), '%Y-%m-%d %H:%M:%S')

    def MonthDatetime():

        return datetime.now(timezone.utc).strftime('%B %d, %Y')