import requests
from bs4 import BeautifulSoup
from mytoken import *
from datetime import datetime
import mydate_sql0

class Parser:
    def __init__(self, url, m):
        headers ={
            "Accept": "*/*",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:106.0) Gecko/20100101 Firefox/106.0",

        }
        req = requests.get(url, headers=headers)
        req.encoding = "utf-8"

        self.m = m
        self.f = 0
        self.en = en
        self.soup = BeautifulSoup(req.text, "lxml")


    def parser(self, page, n, cl):
        arr = []
        try:
            pg =  self.soup.find(class_="pagination").find(class_="el-pager").find_all(class_="number")
        except BaseException:
            return 'END'

        try:
            all2 = [i for i in self.soup.find_all(class_="event-card small-12 grid-x") if i.find(class_="event-card__content small-12 medium-10 grid-x").find(class_="event-card__content-status small-12 grid-x align-middle success") != None]
        except BaseException:
            return 'END'
        for i in all2:
            if int(pg[-1].text) < page:
                return 'END'
            text_date = i.find(class_="event-card__date small-2 grid-y show-for-medium").text.replace("  ", "").replace("\n", " ").replace(" мск", "")
            text_labl = i.find(class_="event-card__content-description-title").text.strip()
            href = i.find(class_="event-card__content-description-title").find(class_="").get("href").strip()
            href = "https://profil.mos.ru/events" + href.replace("\n", "")
            photo = i.find(class_="event-card__content-image small-12 medium-4 align-self-middle").find("img").get("src")
            univer = i.find(class_= "event-card__content-description-agent").text.strip()
            registered = ["", ""]
            if i.find(class_='event-card__content-image-stat grid-x align-spaced align-bottom').find('span', 'el-tooltip event-card__content-image-stat-people event-card__content-image-stat-people') != None:
                registered = (i.find(class_='event-card__content-image-stat grid-x align-spaced align-bottom').find('span', 'el-tooltip event-card__content-image-stat-people event-card__content-image-stat-people').text).strip()
                registered = [registered, "Очно"]
            elif i.find(class_='event-card__content-image-stat grid-x align-spaced align-bottom').find('span', 'el-tooltip event-card__content-image-extramural event-card__content-image-extramural') != None:
                registered = i.find(class_='event-card__content-image-stat grid-x align-spaced align-bottom').find('span', 'el-tooltip event-card__content-image-extramural event-card__content-image-extramural').text.strip()
                registered = [registered, "Онлайн"]
            text_date_for_arr = f'{" ".join(text_date.split()[:3])} {ru[en.index(text_date.split()[3])]}'
            text_date_for_arr= text_date_for_arr.split()[2]+ " " +text_date_for_arr.split()[3]+" " +text_date_for_arr.split()[0]
            date = " ".join(text_date_for_arr.split()[:2])
            hour  = text_date_for_arr.split()[2]
            registered = f"{registered[0]} {registered[1]}"
            arr.append([n, text_labl, date, hour, href, registered, univer, photo])
            n+=1
            print([n, text_labl, date, hour, href, registered, univer, photo])
        cl.add_event(arr)
        m = Manager(self.m, cl)
        return m.manager(page+1, n)

    def req2_1(self, page, n, cl):
        arr = []
        if self.soup.find(class_="GridColstyles__Block-sc-1icdvzs-0 GridCol___StyledBlock-sc-6nxth2-0 ctTxVU yWeVU").find(class_="EventsListItemstyles__Block-sc-1cjxdym-0 EventsListItem__Block-sc-evx395-0 dOdLWZ uIWxK") is None:
            print(22)
            #cl.order_by('id')
            return 'END'
        all_events = self.soup.find(class_="GridColstyles__Block-sc-1icdvzs-0 GridCol___StyledBlock-sc-6nxth2-0 ctTxVU yWeVU").find_all(class_="EventsListItemstyles__Block-sc-1cjxdym-0 EventsListItem__Block-sc-evx395-0 dOdLWZ uIWxK")
        for event in all_events:
            text_labl = event.find(class_="Textstyles__Block-sc-8ry03o-0 iCDSna").text.strip()
            href = "https://www.ucheba.ru"+event.find(class_="Heading__H3-sc-1gjj71t-2 xXyZL").find('a').get("href")
            info = event.find_all(class_="Textstyles__Block-sc-8ry03o-0 jumTHj")
            univer = info[1].find("a").text.strip()
            text_date = info[0].text.replace("МСК", '', 1).replace("•", '', 1).replace("   ", '', 1).replace(",", '',1).replace("2023", "").strip()
            registered = f"-- {text_date.split(' ')[3]}"
            photo = event.find(class_="ExternalLogostyles__Image-sc-1qhivu3-0 ExternalLogo___StyledImage-sc-1kvnpec-0 bmqJPv cpTyGP").get("src")#.replace("background-image: url(", '', 1).replace(");", '', 1)
            hour = text_date.split(" ")[2]
            mount = text_date.split(" ")[1].capitalize()
            if mount in ru_sg:
                mount = ru_sg[mount]
            date = text_date.split(" ")[0] +" "+ mount
            #print(date)
            arr.append([n, text_labl, date, hour, href, registered, univer, photo])
            n+=2
        cl.add_event(arr)
        m = Manager(self.m, cl)
        return m.manager(page+1, n)


    def req2(self, page, n, cl):
        if self.f == 1:
            self.page =0
            self.req2_2(n)
        arr = []
        all_titels = []
        ads = len(self.soup.find_all(class_="card s-height-300"))
        if self.soup.find(class_="cards") == None:
            #print(11)
            m = Manager("m2_1", cl)
            return m.manager(1, 1)
        all_titels = self.soup.find(class_="cards").find_all(class_="card")
        if None in all_titels:
            all_titels.remove(None)
        for i in all_titels:
            if i.find(class_="card-action") != None:
                i = i.find(class_="card-action")
                text_labl = i.find(class_="card-subtitle").text.strip()
                univer = i.find(class_="card-title").text.strip()
                text_date = i.find(class_="card-heading").text.strip()
                href = i.find(class_="card-footer").find_all(class_="btn btn-outline btn-outline-default-primary")
                if len(href) > 1:
                    href = href[1].get("href")
                else:
                    href = href[0].get("href")
                registered = ["", ""]
                photo = ""
                if len(text_date.split()) > 4:
                    text_date = text_date.split()[0]+" "+text_date.split()[1].capitalize()+" "+text_date.split()[6]
                else:
                    text_date = text_date.split()[0]+" "+text_date.split()[1].capitalize()
                registered = f"{registered[0]} {registered[1]}"
                if len(text_date.split()) < 3:
                    date = text_date
                    hour = ''
                else:
                    date = " ".join(text_date.split()[:2])
                    hour  = text_date.split()[2]
                arr.append([n, text_labl, date, hour, href, registered, univer, photo])
                n+=2
        cl.add_event(arr)
        m = Manager(self.m, cl)
        return m.manager(page+1, n)

    def req3(self, page, n, cl):
        arr = []
        all_events = self.soup.find(class_="entry-content").find(class_="ecwd_64 ecwd_theme_calendar_grey calendar_full_content calendar_main").find(class_="ecwd-page-full ecwd_calendar").find(class_="ecwd-page-64").find(class_="ecwd_calendar_container full cal_blue").find(class_="events").find(class_= "0")
        #print(all_events)

    def req4(self, page, n, cl):
        arr = []
        end = len(self.soup.find(class_="paginator mt-25").find_all("a"))
        if end < page:
            return "END"
        all_events = self.soup.find(class_="olympiads").find_all(class_="olympiads__row row")
        for event in all_events:
            text_labl = event.find(class_="olympiads__title").text.strip()
            href = "https://www.ucheba.ru"+event.find(class_="olympiads__img col-md-3 col-sm-12").get("href")
            info = event.find(class_="info").find_all(class_="info__row")
            univer = info[0].find(class_="info__content").text.replace("\t", '').strip()
            lessens = info[1].find(class_="info__content").text.strip()
            text_date = info[2].find(class_="info__content").text.replace("\n\t\t\t\t\t\t\t\t\t\t\t\t", '', 1).strip()
            registered = "   "
            photo = event.find(class_="olympiads__img col-md-3 col-sm-12").get("style").replace("background-image: url(", '', 1).replace(");", '', 1)
            hour = ''
            date = text_date
            arr.append([n, text_labl, date, hour, href, registered, univer, photo])
            n+=1
        cl.add_event(arr)

        m = Manager(self.m, cl)
        return m.manager(page+1, n)

class Manager:
    def __init__(self, tape, cl):
        self.page = 0
        self.tape = tape
        self.cl = cl
    def manager(self, page, n):
        url = dict_url[self.tape].replace("::spots_for_page::", str(page), 1)
        pg = Parser(url, self.tape)
        if self.tape == "m1" or self.tape == "m3":
            return(pg.parser(page, n, self.cl))
        elif self.tape == "m2":
            return(pg.req2(page, n, self.cl))
        elif self.tape == "m5":
            return(pg.req4(page, n, self.cl))
        elif self.tape == "m2_1":
            return(pg.req2_1(page, n, self.cl))
    def exit(self):
        return "end"
