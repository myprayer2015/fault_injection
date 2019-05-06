import _thread
import threading
import time
import sys
import logging


def exhaust_cpu(times=10000000):
    count = 1
    num = 1
    while count < times:
        num = num * 2
        count = count + 1
        if num >= sys.maxsize/2:
            num = 1


if __name__ == '__main__':
    try:
        threads = []
        for i in range(0, 5):
            thread = threading.Thread(target=exhaust_cpu, args=(10000000,))
            threads.append(thread)
        for t in threads:
            t.start()
        for t in threads:
            t.join()
    except Exception as e:
        logging.exception(e)

