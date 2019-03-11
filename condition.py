# -*- coding: utf-8 -*-
# time: 19-3-8 下午4:44
"""
多进程状态下的condition不可用
"""

import multiprocessing
from multiprocessing import Manager
from multiprocessing.managers import BaseManager
import time


class Producer(multiprocessing.Process):
    def __init__(self, con):
        self.condition = con
        super().__init__()

    def run(self):
        global count
        while True:
            if self.condition.acquire():
                print(count)
                if count > 700:
                    self.condition.wait()
                else:
                    count = count+100
                    msg = self.name+' produce 100, count=' + str(count)
                    print(msg)
                    self.condition.notify()
                self.condition.release()
                time.sleep(1)


class Consumer(multiprocessing.Process):
    def __init__(self, con):
        self.condition = con
        super().__init__()

    def run(self):
        global count
        while True:
            if self.condition.acquire():
                if count < 100:
                    self.condition.wait()
                else:
                    count = count-50
                    msg = self.name+' consume 50, count='+str(count)
                    print(msg)
                    self.condition.notify()
                self.condition.release()
                time.sleep(1)


count = 500
# con = multiprocessing.Condition()


class MyManager(BaseManager):
    pass


def test():
    # MyManager.register()
    with Manager() as manager:
        print("address", manager.address)
        print("connect", manager.connect())
        con = manager.Condition()
        for i in range(2):
            p = Producer(con)
            p.start()
        for i in range(2):
            c = Consumer(con)
            c.start()


if __name__ == '__main__':
    test()
