# from urllib.request import urlopen
# from bs4 import BeautifulSoup
# import notify2
from win10toast import ToastNotifier
from requests_html import HTMLSession
import time
import json
import schedule


def cricket_score_scraping():
    session = HTMLSession()

    r = session.get('http://www.espncricinfo.com/scores/')

    scores=r.html.find('body')


    scores_list=[]
    scores_individual=[]
    
    for i in scores:
        if i.find('.cscore_name--long'):
            score=i.find('.cscore_name--long')
            scores_list.extend(score)

        if i.find('.cscore_score '):
            scores_ind=i.find('.cscore_score ')
            scores_individual.extend(scores_ind)

    print(len(scores_list))
    print(len(scores_individual))

    dic=dict()

    for i in range(len(scores_list)):
        if i<=7:
            dic[scores_list[i].text]=scores_individual[i].text

    print(dic)
    ICON_PATH = "cricket.ico"
    toaster = ToastNotifier()
    string=''
    count=0
    for i,j in dic.items():
        count=count+1

        string += str(i) + " "+ str(j) + "\n"
        if count==2:
            toaster.show_toast("scores",
                           string,
                           icon_path=ICON_PATH,
                           duration=2)
            count=0
            string=''

if __name__=="__main__":
    cricket_score_scraping()
    schedule.every(1).minutes.do(cricket_score_scraping)
    while True:
        schedule.run_pending()
        time.sleep(0.1)



