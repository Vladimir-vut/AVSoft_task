import logging

'''Устанавливаем конфигурацию логера, данная конфигурация будет использоваться во всём проекте'''
logging.basicConfig(filename='parser.log',
                    filemode='w',
                    level=logging.DEBUG,
                    format='%(asctime)s - %(filename)s - PROCESS ID:[%(process)d] - THREAD ID:[%(thread)d] '
                           '- THREAD NAME:[%(threadName)s] - '
                           'FUNCTION:[%(funcName)s] - LINE:[%(lineno)d] - %(levelname)s[%(message)s]')


log = logging

