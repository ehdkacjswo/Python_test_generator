def func(a, b, c):
    print abs(a - 1 - 0)
    if a - 1 == 0:
        b = a - c
    else:
        print -abs(a - 0)
        if a != 0:
            c = 1
        else:
            print c - 1
            if c < 1:
                a = 1
            else:
                print 1 - c
                if c > 1:
                    b = 1
                else:
                    print c - 1
                    if c <= 1:
                        b = 1
                    else:
                        print 1 - c
                        if c >= 1:
                            c = 1
                        else:
                            b = 100
    rt = b + c
    return rt


print func(-1, 2, 3)
