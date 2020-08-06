from queue import Queue
from threading import Thread


class Worker(Thread):
    def __init__(self, tasks):
        Thread.__init__(self)
        self.daemon = True
        self.tasks = tasks
        self.start()

    def run(self):
        while True:
            fn, link = self.tasks.get()
            fn(link)
            self.tasks.task_done()


class My_Queue:
    def __init__(self, value_threads):
        self.tasks = Queue(value_threads)
        for _ in range(value_threads):
            Worker(self.tasks)

    def add_to_queue(self, fn, link_list, url):
        for link in link_list:
            link = url+link
            print(link)
            self.tasks.put((fn, link))

    def white_finish(self):
        self.tasks.join()


