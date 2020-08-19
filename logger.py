import logging

'''Устанавливаем конфигурацию логера, данная конфигурация будет использоваться во всём проекте'''
logging.basicConfig(filename='parser.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s : [%(thread)d] [%(process)d] '
                           ':[%(filename)s.%(lineno)d]: %(levelname)s : %(message)s')


log = logging

