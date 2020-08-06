from pars import Link_Parser
from concurrent.futures import ProcessPoolExecutor, as_completed
from trees import My_Tree
from datetime import datetime
import sys


def run(url):
    try:
        # Создается объект для получения ссылок с уже полученных страниц ранее
        th_parser = Link_Parser(url)
        th_parser.get_links()

    except Exception as e:
        print(e)
    return th_parser.link_list


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
    used_links = []

    start = datetime.now()
    while True:
        try:
            with ProcessPoolExecutor() as executor:
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
                    '''Дожидаемся выполнения задач, получаем результат
                    если среди полученных ссылок присутствуют те которых нет в главном списке, то добавляем их'''
                    for i in future_pool.result():
                        if i not in link_parser.link_list:
                            link_parser.link_list.append(i)
            if len(used_links) == len(link_parser.link_list):  # Прекращаем парсинг когда все ссылки пропарсены
                break
            log.info(f'TIME WORKING OF TASKS - {datetime.now() - start}')  # Записывает общее время работы парсера
        except Exception as e:
            log.error(e)

    link_parser.link_list.sort()
    link_parser.make_file_link()

    tree = My_Tree()  # Объект для генерации дерева
    tree.make_tree(link_parser.file_links)  # Генрация дерева
    tree.draw_tree()  # Вывод дерева на экран сохранение в графическом файле
    with open('tree.txt', 'w') as f:  # Сохранение дерева в txt файл
        f.write(f'{tree}')


if __name__ == '__main__':
    '''Из за мультипроцессорности логирование работает криво, очивидно что нужно использовать
        локеры, но пока не разобрался'''
    from logger import log
    main()

