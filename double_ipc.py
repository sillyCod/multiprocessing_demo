# -*- coding: utf-8 -*-
# time: 19-3-8 下午4:20
"""
Pipe可以实现在进程之间传递对象
"""
import time
from multiprocessing import Pipe, Process


def producer(client):
    con = 0
    while True:
        print("producer send:", con)
        client.send(con)
        time.sleep(1)
        con = client.recv()
        print("producer get", con)
        con = con+1


def consumer(server):
    while True:
        con = server.recv()
        print("consumer get", con)
        time.sleep(1)
        server.send(con + 1)
        print("consumer send", con+1)


if __name__ == "__main__":
    cli, server = Pipe()
    p1 = Process(target=producer, args=(cli, ))
    p2 = Process(target=consumer, args=(server, ))
    p2.start()
    p1.start()
