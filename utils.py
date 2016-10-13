import time


def log(*args, **kwargs):
    f = '[%Y/%m/%d %H:%M:%S] '
    value = time.localtime(int(time.time()))
    dt = time.strftime(f, value)
    print(dt, *args, **kwargs)

