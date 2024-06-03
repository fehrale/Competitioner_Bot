from bs4 import BeautifulSoup as bs
import requests
import datetime
import calendar

#from time import time


link = lambda x: 'https://postypashki.ru/ecwd_calendar/calendar/'+'?date='+x+'&t=list'

def get_data(text):
    sp = bs(text,'lxml')
    return sp.find("div", {"class": "event-content"}).text

def pars(d):
    #d = str(time()).split(".")[1][-1:-4:-1]+d
    d = d.split(":")
    try:
        dic = {d[0] : d[1]}
        return dic
    except IndexError:
        return {}
    

def get_year():
    def inc(sd,ms):
        m= sd.month -1 +ms
        y = sd.year + m // 12
        m = m % 12 + 1
        return datetime.date(y,m,min(sd.day, calendar.monthrange(y,m)[1])).strftime('%Y-%m')+'-15'
    res = {}
    [res.update(pars(j)) for j in [get_data(requests.get(u).text) for u in ([link(inc(datetime.date.today(),g)) for g in range(12)])]]
    return res

    
     
     

print(get_year())
    
