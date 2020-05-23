class glob:
	spam = []
	def do_local(self, i):
		glob.spam.append(self)

glob1 = glob()
glob2 = glob()

glob2.do_local(1)
glob1.do_local(2)
print(glob.spam)
