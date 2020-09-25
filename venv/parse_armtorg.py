# Здраствуйте. Я нашел заказ на парсинг контактов с ресурса ARMTORG. Надеюсь вы разрешите выполнить дз по другому ресурсу
# Ресурс armtorg.ru. Нужно спарсить в ексель контакты компаний что продают Фланцы.
import bs4
import requests
import time
# from pymongo import MongoClient

class GbBlogParser:
    __headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:78.0) Gecko/20100101 Firefox/78.0",
    }

    def __init__(self, domain):
        self.domain = domain
        self.post_domain = 'https://armtorg.ru'
        self.start_url = f'{self.domain}'
        self.post_link = set()
        self.urls_pag = set()
        self.done_urls = set()  # множество для уникальности
        self.post_urls = set()
        # self.mo_client = MongoClient('mongodb://localhost:27017')

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
        # print(links)
        return links

    def get_post(self, post):
        for i in post:
            response = requests.get(i, headers=self.__headers)
            for i in response:
                print(i)
        return post
        pass
#
#     # todo найти список постов и вернуть список url на посты

    def get_post_urls(self, soup):
        wrapper = soup.find('div', attrs={'class': "table-responsive"})
        posts = wrapper.find_all('table', attrs={'class': "t1 table table-striped"})

        # links = {f'{self.post_domain}{itm.find_all("td").attrs.get("href")}' for itm in posts if itm.find('a').attrs.get('href')}
        for link in wrapper('a', attrs={'class':False}):   #Получил ссылки на компании.
            link.find_all('href')
            if link.get('title') == None:
                continue
            over_link = f'{self.post_domain}{link.get("href")}'
            # print(over_link)
            # return over_link
            # print(f'{self.post_domain}{link.get("href")}')
            # print(link)

        return over_link


    def parse(self):
        url = self.start_url
        while url:
            soup = self.get_soup(url)  # получаем суп
            self.urls_pag.update(self.get_pagination(soup)) #забераем ссылки на другие страницы
            self.urls_pag.difference_update(self.done_urls) #удаляем то что отработали
            url = self.urls_pag.pop() if self.urls_pag else None # Забераем все ели не none
            self.post_urls.update(self.get_post_urls(soup).split(',')) # Получаем ссылки на посты
            self.get_post(self.post_urls)
            # self.get_post(self.post_urls)
            # print(self.get_post(self.post_urls))
            print(len(self.post_urls))
            print(self.post_urls)
            print(len(self.done_urls))
            time.sleep(1)
            # post = self.get_post(self.post)
#         for itm in self.post_urls:
#             self.save_to_mongo({'url': itm})
        print('hello')
#
#     # todo сохранить в БД
#     def save_to_mongo(self, data: dict):
#         db = self.mo_client['gb_parse_09']
#         collection = db['gb_blog']
#         collection.insert_one(data)
#         print(1)
#

if __name__ == '__main__':
    parser = GbBlogParser('https://armtorg.ru/goods/by-category/Фланцы')
    parser.parse()