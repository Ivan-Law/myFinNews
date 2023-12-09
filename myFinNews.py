import FinNews as fn
from datetime import datetime, timedelta
import pandas as pd

def check0(nn):
    if nn[0] == "0":
        return nn[1:]
    else:
        return nn
    
EndDate1 = datetime.now()
EndDate2 = datetime.now() - timedelta(1)
myNow1 = check0(EndDate1.strftime('%b %d'))
myNow2 = check0(EndDate2.strftime('%b %d'))
myNow3 = check0(EndDate1.strftime('%d %b'))
myNow4 = check0(EndDate2.strftime('%d %b'))
myNow5 = check0(EndDate1.strftime('%m-%d'))
myNow6 = check0(EndDate2.strftime('%m-%d'))
myNow7 = check0(EndDate1.strftime('%m/%d'))
myNow8 = check0(EndDate2.strftime('%m/%d'))

searchfor = [myNow1, myNow2, myNow3, myNow4, myNow5, myNow6, myNow7, myNow8]
myNow = EndDate1.strftime('%Y-%m-%d-%H-%M')
myNews = pd.DataFrame(columns=['published', 'title', 'link'])

def readnews(myNewsName, myNews, rr):
    df = pd.DataFrame(rr)
    yy = df.loc[:,['published','title','link']]    ## select columns
    yy = yy[yy['published'].str.contains('|'.join(searchfor))]
    
    frames = [myNews, yy]
    myNews = pd.concat(frames)
    return myNews
        
inv_news = fn.Investing(topics=['*'], save_feeds=True)
myNews = readnews('Investing-', myNews, inv_news.get_news())

y = fn.Yahoo(topics=['*'])
myNews = readnews('YNews-', myNews, y.get_news())

cnbc_feed = fn.CNBC(topics=['finance', 'earnings'])
myNews = readnews('CNBC-', myNews, cnbc_feed.get_news())

s_feed = fn.SeekingAlpha(topics=['financial'], save_feeds=True)
myNews = readnews('SeekingAlpha-', myNews, s_feed.get_news())

wsj_news = fn.WSJ(topics=['*'], save_feeds=True)
myNews = readnews('WSJ-', myNews, wsj_news.get_news())

red_news = fn.Reddit(topics=['$finance', '$news'])
myNews = readnews('Reddit-', myNews, red_news.get_news())

inv_news = fn.Investing(topics=['*'], save_feeds=True)
myNews = readnews('Investing-', myNews, inv_news.get_news())

ftnews = fn.FT(topics=['*'])
myNews = readnews('FT-', myNews, ftnews.get_news())

fortune = fn.Fortune(topics=['*'])
myNews = readnews('Fortune-', myNews, fortune.get_news())

myNews.set_index('published', inplace=True)

###

from bs4 import BeautifulSoup
import requests

TWNews = 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=zh-TW&gl=TW&ceid=TW%3Azh-Hant'
HKNews = 'https://news.google.com/news/rss/headlines/section/topic/BUSINESS?hl=zh-HK&gl=HK&ceid=HK%3Azh-Hant'

N = [HKNews, TWNews]
myN = []
EndDate1 = datetime.now()
myNow = EndDate1.strftime('%Y-%m-%d-%H-%M')

params = {
    "hl": "zh-HK",         # languages like en-US, zh-TW
    "gl": "HK",            # country of the search, US -> USA
    "ceid": "HK:zh-HK",
}

headers = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/100.0.4896.88 Safari/537.36",
}

def myNewsF(thisNews):
    html = requests.get(thisNews, params=params, headers=headers, timeout=30)
    soup = BeautifulSoup(html.text, "xml")

    for result in soup.channel.find_all('item'):
        title = result.title.text
        link = result.link.text
        myN.append([myNow, title, link])
        
for i in N:
    myNewsF(i)

myN = pd.DataFrame(myN)
myN.columns = ['published', 'title', 'link']
myN.set_index('published', inplace=True)
print(myN)

myNews = pd.concat([myNews, myN])

###

myNews.to_csv('My-Finance-News-' + myNow +'.csv', encoding="utf_8_sig")
print(myNews)