import numpy as np
import random as rand

# Check whether new test is in the given test_list
def in_test(test_list, new_test):
	for test in test_list:
		if test == new_test:
			return True
	
	return False

# If non of given test is identical to new test, add it
def add_test(test_list, new_test):
	if in_test(test_list, new_test):
		return test_list
	
	return test_list + [new_test]

# Mutate given input
def mutate(test, special):
	same = 0

	for ind in range(len(test)):
		prob = rand.random()
		if prob <= 0.05:
			test[ind] -= 1

		elif prob <= 0.1:
			test[ind] += 1

		elif prob <= 0.2:
			test[ind] = rand.choice(special)

		else:
			same += 1
	
	# If none is changed, muteate again
	if same == len(test):
		return mutate(test, special)
	
	return test
