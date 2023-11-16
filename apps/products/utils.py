import datetime


class Util:
    @staticmethod
    def year_dropdown():
        return [(y, y) for y in range(1900, (datetime.datetime.now().year + 10))]
