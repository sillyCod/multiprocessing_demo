# -*- coding: utf-8 -*-
# time: 19-3-12 下午2:19
import time
from threading import Thread, Condition

products = list(range(10))


def producer(condition):
    global products
    while True:
        if condition.acquire():

            if len(products) < 10:
                print("produce")
                products.append(1)
                time.sleep(2)
                condition.notify()
                condition.release()
            else:
                print("producer wait")
                condition.wait()


def consumer(condition):
    global products
    while True:
        if condition.acquire():
            if len(products) >= 10:
                print("consume")
                products = products[:8]
                time.sleep(2)
                condition.notify()
                condition.release()
            else:
                print("consumer wait")
                condition.wait()


if __name__ == "__main__":
    con = Condition()
    t1 = Thread(target=producer, args=(con, ))
    t2 = Thread(target=consumer, args=(con, ))
    t1.start()
    t2.start()
    t1.join()
    t2.join()
    t1.setDaemon(True)
    t2.setDaemon(True)
