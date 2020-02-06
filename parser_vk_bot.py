from my_lib import get_html, save_file
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from datetime import datetime
import random


class Parser:

    def __init__(self):
        self.downl_list = []
        self.E_SITE = 'cp1251'
        self.i_count = 0

    def get_pages(self, html):
        soup = BS(html, features="html.parser")
        img_count = soup.find('div', class_='header-text').find('h2').text
        try:
            r = soup.find('div', class_='navigation').find_all('a')[-2].text
            return int(r), img_count
        except AttributeError:
            return 1, img_count

    def parsing(self, html, obj, win_size_w, win_size_h):
        global i_count
        global downl_list
        soup = BS(html, features="html.parser")
        r = soup.find('div', id='dle-content').find_all('a', class_='screen-link')
        for inc, a in enumerate(r, start=1):
            soup = BS(get_html(a.get('href'), self.E_SITE), features="html.parser")
            req = soup.find('div', class_='llink').find_all('a')
            for aa in req:
                size_w = int(aa.get('href').split('/')[-2].split('x')[0])
                size_h = int(aa.get('href').split('/')[-2].split('x')[1])
                if win_size_w == size_w and win_size_h == size_h:
                    url_size = aa.get('href')
                    self.downl_list.append(url_size)
                else:
                    continue
        random_el = random.choice(self.downl_list)
        soup2 = BS(get_html(random_el, self.E_SITE), features="html.parser")
        image_url = soup2.find(id='img').get('src')
        name = f'img/{obj}' + '.jpg'
        save_file(image_url, name)
        print(f'|{name.split("/")[-1]:^{33}}|{"Загружен":^{10}}|')
        self.i_count += 1
        return self.i_count

    def main(self, obj):

        start_time = datetime.now()
        win_width = 1920
        win_heigth = 1080
        url = f'https://www.nastol.com.ua/tags/{quote(obj.strip(), encoding=self.E_SITE)}/page/1/'
        pages, img_count = self.get_pages(get_html(url, self.E_SITE))
        page = random.randint(1, pages)
        base_url = f'https://www.nastol.com.ua/tags/{quote(obj.strip(), encoding=self.E_SITE)}/page/{page}/'
        print(f'{img_count}\nСтраница:{page}-{pages}')
        print('-' * 51)
        print(f'|{"Категория - имя файла":{33}}|{"Статус":{10}}|')
        print('-' * 51)
        inc = self.parsing(get_html(base_url, self.E_SITE), obj, win_width, win_heigth)
        print('-' * 51, end='\n')
        print(f'Скачано:{inc}')
        end_time = datetime.now()
        print(f'Затрачено времени:{str(end_time - start_time).split(".")[0]:^{50}}')
        print('-' * 51, end='\n')
