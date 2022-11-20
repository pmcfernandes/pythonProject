from datetime import datetime


class Dates:
    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def toDateTime(s):
        return datetime.strptime(s, '%m/%d/%y %H:%M:%S')

