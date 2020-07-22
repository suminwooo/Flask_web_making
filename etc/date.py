from datetime import datetime
def time():
    now = datetime.now()
    time = "%s월 %s일 %s시 %s분" %(now.month, now.day, now.hour, now.minute)
    return time