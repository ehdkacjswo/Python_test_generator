def func(a, b, c):
    ff = open('fitness', 'w')
    tt = a - 0
    ff.write('{} {} {}\n'.format(1, 2, tt))
    if a < 0:
        return 1
