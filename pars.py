from logger import log
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup



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
        log.info(f'START UPLOAD - {self.url}')
        try:
            target_page = urlopen(self.url)
            hostname = urlparse(self.url).hostname
            soup = BeautifulSoup(target_page, 'html.parser', from_encoding="iso-8859-1")
            links = soup.find_all('a')  # Ищет ссылки
            link_list = [l.get('href') for l in links]  # выделяет ссылки
        except Exception as e:
            log.error(e)
            if UnboundLocalError:
                raise SystemExit(1)

        for link in link_list:
            if link:
                for social_net in self.social_nets:
                    if social_net in link:
                        link = '_'
                        continue

                if '?' in link:
                    link = link[:link.find('?')]

                if link and link[0] != '/' and not link.startswith(self.url):
                    link = '_'

                if hostname in link:
                    link = link.split(hostname)
                    link = link[-1]

                if link.startswith('http') and hostname not in link:
                    link = '_'

                if link != '_' and link not in self.link_list and len(link) > 1:
                    self.link_list.append(link)

    def make_file_link(self):  # запись в файл
        with open(self.file_links, 'w', encoding='utf-8') as f:
            for link in self.link_list:
                f.write(link+'\n')







