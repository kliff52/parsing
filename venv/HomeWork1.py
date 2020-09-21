## Не успел выполнить дз. Прошу прощения. Сейчас сижу за выполнением его . Это заглушка.
## Задача организовать сбор данных,
#необходимо иметь метод сохранения данных в .json файлы
#результат: Данные скачиваются с источника, при вызове метода/функции сохранения в файл скачанные данные
#сохраняются в Json вайлы, для каждой категории товаров должен быть создан отдельный файл и содержать
# товары исключительно соответсвующие данной категории.
#пример структуры данных для файла:


#response = requests.get('https://5ka.ru/api/v2/categories/')
#data = response.json()
#payload = {'parent_group_code':'parent_group_name'}
#r = requests.get('https://5ka.ru/api/v2/categories/', data=json.dumps(payload))
#data = r.json()
#print(data)


import json
import time
from copy import copy
from pathlib import Path
import requests


class Parse5ka:
    def __init__(self):
        self.api_url = "https://5ka.ru/api/v2"
        self.endpoint_so_categories = '/categories'
        self.endpoint_so = '/special_offers'
        self.params = {"records_per_page": 100, "page": 1}
        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:80.0) Gecko/20100101 Firefox/80.0',
            'Accept': 'application/json',
        }
    def categories(self):
        url = f'{self.api_url}{self.endpoint_so_categories}'
        while url:
            response = requests.get(url, headers=self.headers)
            if response.status_code >= 500:
                time.sleep(10)
                continue
            data = response.json() # Дата категорий
            self.parse(data)
            time.sleep(2)

    def parse(self, data: dict):
        url = f'{self.api_url}{self.endpoint_so}'
        while url:
            print(url)
            for i in data:
                print(i['parent_group_code'])
                pyload = {"categories": i['parent_group_code']}
                response = requests.get(url, params = pyload, headers=self.headers)
                if response.status_code >= 500:
                    time.sleep(10)
                    continue
                data1 = response.json()  # Дата итемов
                print(data1['results'])
                if len(data1['results']) == 0:
                    continue
                else:
                    print('отпровляю в фаил')
                    self.save_to_file(data1['results'],i['parent_group_name'])
        time.sleep(1)


    def save_to_file(self, data: dict, category: dict):
        print('Принял -----------', data, ' -------------',category)
        file_path = Path('data').joinpath(f"{category}.json")
        with open(file_path, 'w') as file:
            print('Записал-', data, category)
            json.dump(data, file, ensure_ascii=False)


if __name__ == '__main__':
    parser = Parse5ka()
    parser.categories()




