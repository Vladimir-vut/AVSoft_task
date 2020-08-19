from logger import log
from urllib.request import urlopen
from urllib.parse import urlparse
from bs4 import BeautifulSoup
from urllib.parse import quote



class Link_Parser:

    '''
    Это объект рабочая лошадка
    1. Парсит переданный URL
    2. Извлекает все ссылки
    3. Фильтрует мусор, т.е. удаляет внешние ссылки, соцсети
    4. По итогу записывает ссылки из из ощего списка в файл
    '''

    def __init__(self, url, timeout, deep):
        '''
        :param url: URL для парсинга (str)
        :param timeout: Таймаут соеденения с переданнм URL (int)
        :param deep: Глубина проработки ссылок (int)
        '''
        self.url = url
        self.deep = deep
        self.link_list = []
        self.timeout = timeout
        self.file_links = 'file_links.txt'
        self.social_nets = ['#', 'vk', 'ok', 'odnoklassniki', 'twitter',
                            'youtube', 'facebook', 'instagram', 'tel:', 'skype', 'mailto:']

    def get_links(self):
        '''
        Метод для ссылок состраницы, с последующей фильтрацией ссылок на соцсети, внешних ссылок,
        аргументов.
        Сохраняет полученный список в list
        :return: None
        '''
        link_list = []
        log.info('Connection to {}'.format(self.url))
        try:
            target_page = urlopen(self.url, timeout=self.timeout)
        except Exception as e:
            log.error('{} URL: {}'.format(e, self.url))
            return
        hostname = urlparse(self.url).hostname
        soup = BeautifulSoup(target_page, 'html.parser')
        links = soup.find_all('a')  # Поиск ссылок на странице
        for l in links:
            if l.get('href') and l.get('href') != '/':
                link_list.append(l.get('href'))

        for link in link_list:
            if link:
                if len(link) > 0:
                    for social_net in self.social_nets:  # Пропускает ссылки с соцсетями
                        if social_net in link:
                            link = ''
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

                    link = link.split('/')
                    if link[0] == '':
                        link.pop(0)
                    elif link[-1] == '':
                        link.pop(-1)

                    if len(link) > self.deep:
                        link = link[:self.deep]
                    link = '/' + '/'.join(link)

                    if link in self.link_list:
                        continue

                    self.link_list.append(quote(link))

    def make_file_link(self):  # запись в файл
        with open(self.file_links, 'w', encoding='utf-8') as f:
            for link in self.link_list:
                if len(link):
                    f.write(link+'\n')







