def test_me(x):
    ffffff = open('fitness', 'w')
    z = 0
    tttttt = abs(x - 2)
    ffffff.write('{} {} {}\n'.format(1, 0, tttttt))
    if x == 2:
        print '1'
        return z
    for i in range(x):
        print '2'
        z += 1
    else:
        print '3'
        if z == 0:
            print '4'
            return x
        while z > 0:
            print '5'
            z -= 1
    return z
