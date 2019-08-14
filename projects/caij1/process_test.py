from multiprocessing import Process
import time
import random

from multiprocessing import Process
import time

x = 0


class DataB(object):
    def __init__(self):
        self.num = 0
        self.p = []

    def change(self):
        if self.num == 0:
            self.num = 1
        else:
            self.num = 0


class Myprocess(Process):
    def run(self):
        while True:
            print('----')
            time.sleep(0.01)


db = DataB()


def run_main():
    for k in range(len(db.p)):
        if db.p[k].is_alive():
            db.p[k].terminate()
            db.p[k].join()
        time.sleep(0.01)
    db.change()
    print(db.num)
    if db.num == 0:
        new = Myprocess()
        new.start()
        db.p.append(new)
    time.sleep(0.01)


if __name__ == '__main__':
    while True:
        run_main()


# if __name__ == '__main__':
#     while True:
#         x = int(input('?'))
#         if x % 2 == 0:
#             dc.p.terminate()
#         else:
#             dc.p.start()
# must use main








