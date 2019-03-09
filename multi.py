# -*- coding: utf-8 -*-
# time: 19-3-8 上午10:09
import multiprocessing
import time
import cv2
from multiprocessing import Event
from multiprocessing import Pipe, Pool, Manager
from multiprocessing.managers import BaseManager

ready = 0b001
ready2 = 0b011
perfect = 0b111
num = 10


class A:
    pass


class B(A):
    pass

# class Events:
#
#     def __init__(self, event, params):
#         self.event = event
#         self.params = params
#         self.conditions= dict.fromkeys(self.params, False)
#         super().__init__()
#
#     def set(self, func):
#         self.conditions[func.__name__] = True
#         print(self.conditions)
#
#         if all(self.conditions.values()):
#             return self.event.set()
#
#     def wait(self):
#         return self.event.wait()


class Events:

    def __init__(self, event, params):
        self.event = event
        self.params = params
        self.conditions = dict.fromkeys(self.params, False)
        super().__init__()
        print("I'm called")

    def set(self, func):
        self.conditions[func.__name__] = True
        print(id(self.conditions))
        print(self.conditions)

        if all(self.conditions.values()):
            return self.event.set()

    def wait(self):
        return self.event.wait()


cli, server = Pipe()


def producer(e, client, n):
    import time
    time.sleep(5)
    n = n + 1
    d = dict(a=1)
    print("dict address", id(d))
    client.send(d)
    print(id(e))
    e.set()
    print("I'm a producer!")


def consumer(e, ser, n):
    e.wait()

    # global num
    print("I'm a consumer!")
    print(id(e))
    _temp = ser.recv()
    print("temp address", id(_temp))
    # num = n + 1
    return 100


def consumer1(event):
    print("c1", id(event), id(event.conditions))
    print(multiprocessing.current_process().ident)
    event.wait()
    print("I've consumed all")


def producer1(event):
    time.sleep(5)
    print("p1", id(event), id(event.conditions))
    print(multiprocessing.current_process().ident)
    event.set(producer1)
    print("I'm producer1")


def producer2(event):
    time.sleep(10)
    print("p2", id(event), id(event.conditions))
    print(multiprocessing.current_process().ident)
    event.set(producer2)
    print("I'm producer2")


class Observer:
    subscriber = []

    def notify(self):
        for sub in self.subscriber:
            sub.do()


if __name__ == "__main__":
    event = multiprocessing.Event()
    mg = BaseManager()
    mg.start()
    _events = Manager().Event()

    mg.register('Events', Events)

    events = mg.Events(_events, [producer1.__name__, producer2.__name__])
    # p = multiprocessing.Process(target=consumer, args=(event, cli, num))
    # p.start()
    # p1 = multiprocessing.Process(target=producer, args=(event, server, num))
    # p1.start()
    # p.join()
    # p1.join()
    # print(bin(ready & perfect))
    # print(bin(ready2 & perfect))
    p2 = multiprocessing.Process(target=producer1, args=(events, ))
    p3 = multiprocessing.Process(target=producer2, args=(events, ))
    p4 = multiprocessing.Process(target=consumer1, args=(events, ))
    p4.start()
    p2.start()
    p4.join()
    p2.join()
    p3.start()
    p3.join()
        # p4.start()
    # print(num)

    # print(pow(2, 1))
