from datetime import datetime

now = datetime.now()

class date_method:

    def time(self):
        time = "%s월 %s일 %s시 %s분" %(now.month, now.day, now.hour, now.minute)
        return time

    def date(self):
        date = "%s년 %s월 %s일" %(now.year, now.month, now.day)
        return date

    def date_num(self):
        if now.month in ['10','11','12']:
            if len(str(now.day)) == 1:
                date = "%s-%s-0%s" % (now.year, now.month, now.day)
            else:
                date = "%s-%s-%s" % (now.year, now.month, now.day)
        else:
            if len(str(now.day)) == 1:
                date = "%s-0%s-0%s" % (now.year, now.month, now.day)
            else:
                date = "%s-0%s-%s" %(now.year, now.month, now.day)
        return date


