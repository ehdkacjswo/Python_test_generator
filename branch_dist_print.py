def test_me(ff, a, b, c):
    d = 0
    tt = b + c - a
    ff.write('{} {} {}\n'.format(1, 3, tt))
    if a > b + c:
        print '1'
        tt = -abs(b - c)
        ff.write('{} {} {}\n'.format(2, 1, tt))
        if b != c:
            print '2'
            d += 1
        else:
            print '3'
            d += 2
    else:
        print '4'
        d = d - 1
    tt = 0 - d
    ff.write('{} {} {}\n'.format(3, 3, tt))
    if d > 0:
        print '5'
        tt = 0 - a
        ff.write('{} {} {}\n'.format(4, 3, tt))
        if a > 0:
            print '6'
            return 1
        else:
            print '7'
            return 2
    else:
        print '8'
        return 3
