from datetime import datetime


class Date:
    @staticmethod
    def now():
        return datetime.now()

    @staticmethod
    def toDateTime(s: str):
        return datetime.strptime(s, '%m/%d/%y %H:%M:%S')

