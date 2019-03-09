# -*- coding: utf-8 -*-
# time: 19-3-9 下午2:41
from multiprocessing import Manager, Process, Queue
from multiprocessing.managers import BaseManager


class A:
    def __init__(self, name: str, age: int):
        self.name = name
        self.age = age


def change_age(a: A):
    a.age = a.age + 10
    print(a.age)


if __name__ == "__main__":
    manager = Manager()
    with Manager() as manager:
        # manager.start()
        manager.register("A", A)
        print(manager._registry['A'])
        a = manager.A("zhangsan", 10)
        # a = manager._registry["A"][0]("zhangsan", 10)
        p = Process(target=change_age, args=(a, ))
        p.start()
        p.join()
        print(a.age)
