def func(a, b, c):
	if a-1 == 0:
		b = a - c	
	elif a != 0:
		c = 1
	elif c < 1:
		a = 1
	elif c > 1:
		b = 1
	elif c <= 1:
		b = 1
	elif c >= 1:
		c = 1
	else:
		b =  100

	rt = b + c
	return rt

print(func(-1, 2, 3))
