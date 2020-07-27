from datetime import datetime

now = datetime.now()

def time():
    time = "%s월 %s일 %s시 %s분" %(now.month, now.day, now.hour, now.minute)
    return time

def date():
    date = "%s년 %s월 %s일" %(now.year, now.month, now.day)
    return date

def date_num():
    if now.month in ['10','11','12']:
        date = "%s-%s-%s" % (now.year, now.month, now.day)
    else:
        date = "%s-0%s-%s" %(now.year, now.month, now.day)
    return date