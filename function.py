def ma(a, b):
    return a + b

def func(a, b, c):
    if a-1 < 0:
        b, a = 1, 2
    elif a < 0:
        c = 1
    elif c < 1:
        a = 1
    else:
        b = 1

    rt = ma(b, c)
    return rt

func(-1, 2, 3)
