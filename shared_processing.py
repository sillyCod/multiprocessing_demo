# -*- coding: utf-8 -*-
# time: 19-3-8 下午6:14
import multiprocessing


def func(my_dict, my_list):
    my_dict["index1"] = "aaaaaa"  # 子进程改变dict,主进程跟着改变
    my_dict["index2"] = "bbbbbb"
    my_list.append(11)  # 子进程改变List,主进程跟着改变
    my_list.append(22)
    my_list.append(33)


if __name__ == "__main__":
    with multiprocessing.Manager() as MG:  # 重命名
        mydict = multiprocessing.Manager().dict()  # 主进程与子进程共享这个字典
        mylist = multiprocessing.Manager().list(range(5)) # 主进程与子进程共享这个List
        # myobject = multiprocessing.Manager().register()

        p = multiprocessing.Process(target=func, args=(mydict, mylist))
        p.start()
        p.join()

        print(mylist)
        print(mydict)
