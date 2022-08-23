import time

def sleep(sec):
    time.sleep(sec)
def getTimeString():
    t = time.localtime()
    return "%d년 %d월 %d일 %d시 %d분 %d초" % (t.tm_year, t.tm_mon, t.tm_mday, t.tm_hour, t.tm_min,t.tm_sec)
    