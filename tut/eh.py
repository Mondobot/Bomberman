def ceva(x, y):
	a = x[0] - y[0]
	b = x[1] - y[1]

	return a*a + b*b


print ceva((0, 0), (4, 4))
