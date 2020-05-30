def func(a, b, c):
    ff = open('fitness', 'w')
    tt = f(a) - 0
    ff.write('{} {} {}\n'.format(1, 3, tt))
    if f(a) < 0:
        tt = b - 0
        ff.write('{} {} {}\n'.format(2, 3, tt))
        if b < 0:
            return 2
        return 1
    else:
        tt = 0 - b
        ff.write('{} {} {}\n'.format(3, 3, tt))
        if b > 0:
            tt = c - 0
            ff.write('{} {} {}\n'.format(4, 3, tt))
            if c < 0:
                return 2
            else:
                tt = b - 0
                ff.write('{} {} {}\n'.format(5, 3, tt))
                if b < 0:
                    return 4
                else:
                    return 3


def f(a):
    return a
