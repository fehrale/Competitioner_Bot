from bs4 import BeautifulSoup as bs
import requests as re


link0 = 'https://olimpiada.ru/article/1085#math'
link1 = "https://olimpiada.ru/"

def get():
    with open("data.txt") as fu:
        def ch(q):
            return 'Наименование' not in q and 'Уровень' not in q
    
        text = re.get(link0).text
        sp = bs(text,'lxml')
        al = sp.find_all("tr")
        al1 = [u.find_all('td') for u in al]
        al1 = [[q[0].text[1:-1],q[2].text[1:-1],link1 + q[0].find('a', href=True)['href']] for q in al1[14:] if ch(q) and q[0].find('a', href=True) != None]
        dic = {}
        for k in al1:
            dic[k[0]] = k[1:]
        return dic
        
print(get())
