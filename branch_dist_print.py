def test_me(x, y, z):
    ff = open('fitness', 'w')
    a = 0
    b = 0
    c = 0
    tt = abs(x - 4)
    ff.write('{} {} {}\n'.format(1, 0, tt))
    if x == 4:
        print '1'
        a += 1
        tt = abs(x + y - 100)
        ff.write('{} {} {}\n'.format(2, 0, tt))
        if x + y == 100:
            print '2'
            a += 1
            tt = 112831829389 - z
            ff.write('{} {} {}\n'.format(3, 3, tt))
            if z > 112831829389:
                print '3'
                a += 1
            else:
                print '4'
        else:
            tt = abs(x + y - 40)
            ff.write('{} {} {}\n'.format(4, 0, tt))
            if x + y == 40:
                print '5'
    ff.close()
