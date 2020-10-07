# Здраствуйте. Я нашел заказ на парсинг контактов с ресурса ARMTORG. Надеюсь вы разрешите выполнить дз по другому ресурсу
# Ресурс armtorg.ru. Нужно спарсить в ексель контакты компаний что продают Фланцы.
import bs4
import requests
import time
import pandas as pd
from database import GBBlogDB

# from pymongo import MongoClient

class GbBlogParser:
    __headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    def __init__(self, domain):
        self.domain = domain
        self.post_domain = 'https://armtorg.ru'
        self.start_url = f'{self.domain}'
        self.post_link_done = set()
        self.date = set()
        self.post_link = set()
        self.urls_pag = set()
        self.done_urls = set()  # множество для уникальности
        self.post_urls = set()
        # self.mo_client = MongoClient('mongodb://localhost:27017')
        self.alchemy_db = GBBlogDB('sqlite:///armtorg.db')

    def get_soup(self, url):
        # todo сделать обработку статус кодов и ошибок
        response = requests.get(url, headers=self.__headers)
        soup = bs4.BeautifulSoup(response.text, 'lxml')   # Читаем текстом респоунс,
        self.done_urls.add(url)
        return soup
#
    def get_pagination(self, soup):
        ul = soup.find('ul', attrs={'class': "pagination pagination-sm"})
        li = ul.find_all('li')
        links = {f'{self.domain}{itm.find("a").attrs.get("href")}' for itm in li if itm.find('a').attrs.get('href')}
        return links

    def post_parse(self, soup, url) -> dict:
        contact = soup.find_all('table', attrs = {'class':"goods-item__table"})
        var=[]
        for r in contact:
            cont = r.find_all('strong')
            dlin = (len(cont))
            # print(dlin)
            for text in r.find_all(text= True):
                if text == '\n':
                    continue
                var.append(text)
        if dlin == int(7):
            print(dlin)
            post_data = {
                'name': soup.find('h1').text,
                'date': soup.find('div', attrs = {'class':"col-md-12"}).text,
                'adres': var[1:2],
                'city': var[3:4],
                'pos_addres-': var[5:6],
                'telephone- ': var[7:10],
                'kontakt person ': var[11:12],
                'site': var[17:18],
                'url': url,
            }
            # print(post_data)
        if dlin == int(6):
            print(dlin)
            post_data = {
                'name': soup.find('h1').text,
                'date': soup.find('div', attrs={'class': "col-md-12"}).text,
                'adres': var[1:2],
                'city': var[3:4],
                'pos_addres-': var[5:6],
                'telephone- ': var[7:9],
                'kontakt person ': var[10:11],
                'site': var[14:15],
                'url': url,
            }
            # print(post_data)
        if dlin == int(5):
            print(dlin)
            post_data = {
                'name': soup.find('h1').text,
                'date': soup.find('div', attrs={'class': "col-md-12"}).text,
                'adres': var[1:2],
                'city': var[3:4],
                'pos_addres-': None,
                'telephone- ':var[5:7],
                'kontakt person ': var[8:9],
                'site': var[12:13],
                'url': url,
            }
        if dlin == int(4):
            print(dlin)
            post_data = {
                'name': soup.find('h1').text,
                'date': soup.find('div', attrs={'class': "col-md-12"}).text,
                'adres': var[1:2],
                'city': var[3:4],
                'pos_addres-': None,
                'telephone- ': var[5:6],
                'kontakt person ': var[7:8],
                'site': var[8:9],
                'url': url,
            }
        # print(post_data)
        return post_data

        # def get_post(self, post):
        #     for i in post:
        #         response = requests.get(i, headers=self.__headers)
        #         soup = bs4.BeautifulSoup(response.text, 'lxml')
        #         da = []
        #         name = soup.find('h1', attrs={'class': "companies-title margin-top_none"}).contents
        #         date_udate = soup.find('table', attrs= {'class': "goods-item__table"}).text.split("\n")
        #         for itm in date_udate:
        #             if itm == '' and 'Прайс лист компании':
        #                 continue
        #             else:
        #                 da.append(itm)
        #     return name, da
#     # todo найти список постов и вернуть список url на посты

    def get_post_urls(self, soup):
        links = set()
        for i in soup:
            wrapper = soup.find('div', attrs={'class': "table-responsive"})
            for link in wrapper('a', attrs={'class':False}):   #Получил ссылки на компании.
                for i in link.get('href').split(','):
                    if link.get('title') == None:
                        continue
                    over_link = f'{self.post_domain}{i}'
                    links.add(over_link)
        return links

    def parse(self):
        url = self.start_url
        # date = []
        while url:
            soup = self.get_soup(url)  # получаем суп
            self.urls_pag.update(self.get_pagination(soup)) #забераем ссылки на другие страницы
            self.urls_pag.difference_update(self.done_urls) #удаляем то что отработали
            url = self.urls_pag.pop() if self.urls_pag else None # Забераем все ели не none
            self.post_urls.update(self.get_post_urls(soup))  # Получаем ссылки на посты
            for itm in self.post_urls:
                # x = []
                # x.append(a)
                if itm in self.post_link_done:
                    continue
                else:
                    post_soup = self.get_soup(itm)
                    # print(post_soup)
                    post_data = self.post_parse(post_soup, itm)
                    self.alchemy_db.save_post_from_dict(post_data)
                    # print(post_data)
                    # for i in contact.find_all('td', attrs={'class': "field"}).text)
                    # self.alchemy_db.save_post_from_dict(post_data)
            #         date.append(self.get_post(x))
            #         self.post_link_done.add(a)  # Записываем то что мы уже прошли
            # print(len(self.post_link_done))
            # print(date)
            # self.save_to_exel(date)
            time.sleep(2)
            # print()
        print('hello')

    # todo сохранить в БД
    def save_to_exel(self, data):
        df = pd.DataFrame(data)
        writer = pd.ExcelWriter('write.xlsx', engine='xlsxwriter')
        df.to_excel(writer, 'Sheet1')
        writer.save()
        print('Сохранено')

if __name__ == '__main__':
    parser = GbBlogParser('https://armtorg.ru/goods/by-category/Фланцы')
    parser.parse()