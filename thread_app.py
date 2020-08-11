from logger import log
from pars import Link_Parser
from concurrent.futures import ThreadPoolExecutor, as_completed
from trees import My_Tree
from datetime import datetime
import sys


def main():
    # Объект log используется для записи логов
    log.info('START SESSION')

    '''Чтение параметра из консоли, если параметр не задан 
    используется значение по умолчанию'''
    base_url = sys.argv
    if len(base_url) == 2:
        base_url = sys.argv[1]
    else:
        base_url = 'https://www.guidedogs.com'

    # Создание объекта для парсинга главной страницы
    link_parser = Link_Parser(base_url)
    link_parser.get_links()  # Получение ссылок на странице

    log.info('LINKS ON START PAGE:')
    for link in link_parser.link_list:
        log.info(f'{link}')

    def run(url):

        log.info(f'RUN URL: {url}')
        try:
            # Создается объект для получения ссылок с уже полученных страниц ранее
            th_parser = Link_Parser(url)
            th_parser.get_links()

            '''link_parser.link_list основной список ссылок'''
            for link in th_parser.link_list:
                if link:
                    if link not in link_parser.link_list:
                        link_parser.link_list.append(link)
                        log.info(f'ADD LINK - {link}')
        except Exception as e:
            log.error(e)

    used_links = []  # Сюда будут сохраняться ссылки парсинг по которым уже был
    start = datetime.now()
    while True:
        workers = len(link_parser.link_list) - len(used_links) # Определение оптимального числа потоков
        try:
            with ThreadPoolExecutor(max_workers=workers) as executor:
                future_list = []
                for link in link_parser.link_list:
                    if link not in used_links:
                        used_links.append(link)
                        url = f'{base_url}{link}'
                        future = executor.submit(run, url)  # Создаем очередь с задачами, каждой задаче
                                                            # передается свой аргумент
                        future_list.append(future)
                        log.info(f'ADD TASK - {future_list[-1]}')
                for future_pool in as_completed(future_list):
                    future_pool.result()  # Дожидаемся выполнения задач, получаем результат,
                                          # в данном случае все результаты будут None, т.к. run ничего не возвращает
            if len(used_links) == len(link_parser.link_list):  # Прекращаем парсинг когда все ссылки пропарсены
                break
        except Exception as e:
            log.error(e)
            if e == ValueError:
                '''Если количество процессов (max_workers) <= 0 выходим из скрипта,
                т.е. на странице нет ни одной внутренней ссылки'''
                raise SystemExit(1)

    log.info(f'TIME WORKING OF TASKS - {datetime.now()-start}')  # Записывает общее время работы парсера

    link_parser.link_list.sort()
    print('MAKE')
    link_parser.make_file_link()

    tree = My_Tree()  # Объект для генерации дерева
    tree.make_tree(link_parser.file_links)  # Генрация дерева
    tree.draw_tree()  # Вывод дерева на экран сохранение в графическом файле
    with open('tree.txt', 'w') as f:  # Сохранение дерева в txt файл
        f.write(f'{tree}')


if __name__ == '__main__':
    main()

