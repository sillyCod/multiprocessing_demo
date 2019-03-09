# -*- coding: utf-8 -*-
# time: 19-3-9 下午3:32
from multiprocessing.managers import BaseManager
from multiprocessing import Manager
from multiprocessing import Process


class MathsClass(object):
    def __init__(self, x, y):
        self.x = x
        self._y = y

    def y(self):
        return self._y

    def add(self):
        self._y += 10
        print(self.x, self._y)
        return self.x + self._y

    def mul(self):
        print(self.x, self._y)
        return self.x * self._y


class MyManager(BaseManager):
    pass


if __name__ == '__main__':
    MyManager.register('Maths', MathsClass)
    manager = MyManager()
    manager.start()
    maths = manager.Maths(2, 3)
    p = Process(target=maths.add)
    p.start()
    p.join()

    print(maths.add())         # prints 7
    print(maths.mul())
    print(maths.y())
    manager.shutdown()
