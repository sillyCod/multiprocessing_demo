# -*- coding: utf-8 -*-
# time: 19-3-11 下午3:28
from multiprocessing import Process, current_process
from multiprocessing.managers import BaseManager


class Demo(Process):

    def __init__(self, instance):
        self.instance = instance
        super().__init__()

    def run(self):
        print(self.instance.get("x"))

        print("current process id is ", current_process().ident)
        print("instance id is ", id(self.instance))
        print(self.instance.get("process_ident"))

        self.instance.set('process_ident', current_process().ident)


class MyManager(BaseManager):
    pass


class Digit:
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def get(self, key):
        return self.__dict__.get(key)

    def set(self, key, value):
        setattr(self, key, value)

    def get_dict(self):
        return self.__dict__


if __name__ == "__main__":
    MyManager.register("Digit", Digit)
    with MyManager() as manager:
        digit = manager.Digit(1, 2)
        d1 = Demo(digit)
        d1.start()
        d2 = Demo(digit)
        d2.start()
        d1.join()
        d2.join()
        print(digit.get_dict())
