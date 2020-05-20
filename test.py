def func(a, b, c):
    b = 3
    if a - 1 < 0:
        print a - 1 - 0
        b = 3
    elif a < 0:
        c = 1
    elif c < 1:
        a = 1
    else:
        b = 1
    rt = b + c
    return rt


print func(-1, 2, 3)
