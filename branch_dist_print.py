def func(a, b, c):
    fffff = open('fitness', 'w')
    ttttt = abs(a - 1 - 0)
    fffff.write('{} {} {}\n'.format(0, 0, ttttt))
    if a - 1 == 0:
        b = a - c
    else:
        ttttt = -abs(a - 0)
        fffff.write('{} {} {}\n'.format(1, 1, ttttt))
        if a != 0:
            c = 1
        else:
            ttttt = c - 1
            fffff.write('{} {} {}\n'.format(2, 2, ttttt))
            if c < 1:
                a = 1
            else:
                ttttt = 1 - c
                fffff.write('{} {} {}\n'.format(3, 2, ttttt))
                if c > 1:
                    b = 1
                else:
                    ttttt = c - 1
                    fffff.write('{} {} {}\n'.format(4, 3, ttttt))
                    if c <= 1:
                        b = 1
                    else:
                        ttttt = 1 - c
                        fffff.write('{} {} {}\n'.format(5, 3, ttttt))
                        if c >= 1:
                            c = 1
                        else:
                            b = 100
	rt = b + c
	return rt


print func(-1, 2, 3)
