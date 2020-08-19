from logger import log
from pars import Link_Parser
from concurrent.futures import ThreadPoolExecutor, as_completed
from trees import My_Tree
from datetime import datetime
from urllib.request import urlopen
import argparse
from threading import RLock
import re


lock = RLock()  # Замок для ограничения доступа к общим ресурсам сразу несколькими потоками


def run(url, tm, deep):
    '''
    Функуия для парсинга переданного ей URL с последующим сохранением в список
    :param url: URL для парсинга (str)
    :param tm: Таймаут соеденения с переданнм URL (int)
    :param deep: Глубина проработки ссылок (int)
    :return: Список найденных ссылок (list)
    '''
    try:
        # Создается объект для получения ссылок с уже полученных страниц ранее
        th_parser = Link_Parser(url, tm, deep)
        th_parser.get_links()

    except Exception as e:
        log.error(e)
    return th_parser.link_list


def genarate_threads(link_list, base_url, tm, deep, max_links):
    '''
    Функция для генерации потоков с передачей им функции run и её аргументов
    :param link_list: Список ссылок с главной страницы (list)
    :param base_url: URL домена парсинг которого проводится (str)
    :param tm: Таймаут соеденения с переданнм URL (int)
    :param deep: Глубина проработки ссылок (int)
    :param max_links: Количество найденных ссылок при котором прекращается парсинг (int)
    :return: None
    '''
    used_links = []
    while True:
        if len(link_list) > max_links:  # Прекращаем парсинг когда достигнут лимит по ширине парсинга
            break
        if len(used_links) == len(link_list):  # Прекращаем парсинг когда все ссылки пропарсены
            break
        try:
            with ThreadPoolExecutor() as executor:
                future_list = []
                for link in link_list:
                    if link not in used_links:
                        used_links.append(link)
                        url = f'{base_url}{link}'
                        future = executor.submit(run, url, tm, deep)  # Создаем очередь с задачами, каждой задаче
                        log.info("List of args from process {} :  {}".format(future, url))
                        future_list.append(future)
                for future_pool in as_completed(future_list):
                    if len(link_list) > max_links:
                        break
                    '''Дожидаемся выполнения задач, получаем результат
                    если среди полученных ссылок присутствуют те которых нет в главном списке, то добавляем их'''
                    for link in future_pool.result():
                        if link:
                            lock.acquire()
                            if link not in link_list:  # link_parser.link_list основной список ссылок
                                try:
                                    '''Проверка является ли объект html страницей'''
                                    if 'text/html' not in urlopen(base_url + link, timeout=tm).info()['Content-Type']:
                                        lock.release()
                                        continue
                                except Exception as e:
                                    log.error('{} URL: {}'.format(e, base_url + link))
                                    lock.release()
                                    continue

                                link_list.append(link)
                                log.info('add link to general list - {}'.format(link))
                            lock.release()
                            if len(link_list) > max_links:
                                break
        except Exception as e:
            log.error(e)
    return


def main(base_url, tm, deep, max_links):
    '''
    Запускает парсинг ссылок с главной страницы, запускает функцию генерирования процессов,
    запускает построение дерева, и сохранения его в txt файл
    :param base_url: URL домена парсинг которого проводится (str)
    :param tm: Таймаут соеденения с переданнм URL (int)
    :param deep: Глубина проработки ссылок (int)
    :param max_links: Количество найденных ссылок при котором прекращается парсинг (int)
    :return: None
    '''

    log.info('START SESSION')

    '''Чтение параметра из консоли, если параметр не задан 
    используется значение по умолчанию'''

    link_parser = Link_Parser(base_url, tm, deep)  # Создание объекта для парсинга главной страницы
    link_parser.get_links()  # Получение ссылок на странице

    start = datetime.now()

    genarate_threads(link_parser.link_list, base_url, tm, deep, max_links)

    log.info(f'TIME WORKING OF TASKS - {datetime.now()-start}')  # Записывает общее время работы парсера

    link_parser.link_list.sort()
    link_parser.make_file_link()

    tree = My_Tree()  # Объект для генерации дерева
    tree.make_tree(link_parser.file_links)  # Генрация дерева
    tree.draw_tree()  # Вывод дерева на экран сохранение в графическом файле
    with open('tree.txt', 'w') as f:  # Сохранение дерева в txt файл
        f.write(f'{tree}')


if __name__ == '__main__':
    pattern = r'^(https?:\/\/)?([\w\-\.]+)\.([a-z]{2,6}\.?)(\/[\w\.]*)*\/?$'  # Регулярка для проверки URL

    '''Считывание аргументов при запуске скрипта'''
    arguments = argparse.ArgumentParser(description='Arguments of the parser')
    arguments.add_argument('-u', type=str, default='https://www.guidedogs.com',
                           help='URL for parsing. Default URL == https://www.guidedogs.com')
    arguments.add_argument('-tm', type=int, default=1, help='Timeout (sec) to connection to the server')
    arguments.add_argument('-d', type=int, default=1000, help='Depth of parsing, default == 1000 (full parsing)')
    arguments.add_argument('-ml', type=int, default=1000, help='Max width of parsing, default == 20000')
    argument = arguments.parse_args()

    if re.findall(pattern, argument.u):  # Проверка правильности переданного URL
        print('Start parsing {}'.format(argument.u))
        main(argument.u, argument.tm, argument.d, argument.ml)
    else:
        print('Bad URL, please input URL like as http://domain.com')



