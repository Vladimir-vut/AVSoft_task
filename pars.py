from logger import log
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
import re


class Link_Parser:

    '''
    Это объект рабочая лошадка
    1. Парсит корневую страницу сайта
    2. Извлекает все ссылки
    3. Фильтрует мусор, т.е. удаляет внешние ссылки, соцсети
    4. Добавляет ссылку в общий список если её там уже нет
    5. По итогу записывает ссылки из из ощего списка в файл
    '''

    def __init__(self, url):
        self.url = url
        self.link_list = []
        self.file_links = 'file_links.txt'
        self.social_nets = ['#', 'vk', 'ok', 'odnoklassniki', 'twitter',
                            'youtube', 'facebook', 'instagram', 'tel', 'skype']

    def get_links(self):
        log.info('Connection to {}'.format(self.url))
        try:
            target_page = urlopen(self.url)
            hostname = urlparse(self.url).hostname
            soup = BeautifulSoup(target_page, 'html.parser', from_encoding="iso-8859-1")
            links = soup.find_all('a')  # Ищет ссылки
            link_list = [l.get('href') for l in links if l.get('href') != '/']  # выделяет ссылки
        except Exception as e:
            log.error('ERROR: {} URL: {}'. format(e, self.url))
            if UnboundLocalError:
                raise SystemExit(1)

        for link in link_list:
            if len(link) > 0:
                log.info('link - {}'.format(link))  # TODO Декодировать названия линков
                for social_net in self.social_nets:  # Пропускает ссылки с соцсетями
                    if social_net in link:
                        continue

                if '?' in link:  # Убирает аргументы в ссылках
                    link = link[:link.find('?')]

                if hostname in link:  # Отделяет домен
                    link = link.split(hostname)
                    link = link[-1]

                if len(link) < 1:
                    continue

                if link.startswith('http') and hostname not in link:  # Пропускает внешние ссылки
                    continue

                if link[0] != '/':
                    link = '/' + link

                if link not in self.link_list:  # Добавляет ссылку в общий список если она уникальна
                    self.link_list.append(link)

    def make_file_link(self):  # запись в файл
        with open(self.file_links, 'w', encoding='utf-8') as f:
            for link in self.link_list:
                f.write(link+'\n')







