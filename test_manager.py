# -*- coding: utf-8 -*-
# time: 19-3-9 下午3:32
from multiprocessing.managers import BaseManager
from multiprocessing import Manager, current_process
from multiprocessing import Process


class MathsClass(object):
    def __init__(self, x, y):
        self._x = x
        self._y = y

    def x(self):
        return self._x

    def y(self):
        return self._y

    def add(self):
        self._y += 10
        # print(self._x, self._y)
        print("add", current_process().ident)
        print("instance is ", id(self))
        return self._x + self._y

    def mul(self):
        # print(self._x, self._y)
        print("multi", current_process().ident)
        print(id(self))
        return self._x * self._y

    def increase(self):
        print("increase", current_process().ident)
        print("instance is ", id(self))
        self._x += 10
        self._y += 100


class MyManager(BaseManager):
    pass


if __name__ == '__main__':
    MyManager.register('Maths', MathsClass)
    manager = MyManager()
    manager.start()
    maths = manager.Maths(2, 3)
    p = Process(target=maths.add)
    p2 = Process(target=maths.increase)
    p.start()
    p2.start()
    p.join()
    p2.join()

    print(maths.add())         # prints
    print("multi is", maths.mul())
    print(maths.x())
    print(maths.y())
    manager.shutdown()
