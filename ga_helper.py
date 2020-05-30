import numpy as np
import random as rand

def crowd_sel(output, p):
	if p == 0:
		return []
	


# 0: test1 dominates, 1: test2 dominates, 2: non-dominating
def dom(test1, test2, leaf_index):
	# Whether test1 or test2 dominates
	dom1 = False
	dom2 = False

	for key in leaf_index:
		if test1[key] > test2[key]:
			dom2 = True
		elif test2[key] > test1[key]:
			dom1 = True

		if dom1 and dom2:
			return 2
	
	if dom1:
		return 0
	
	elif dom2:
		return 1

# Apply non dominated sorting and select by crowd distance
def pop_sel(output, leaf_index, p):
	'''if len(output) <= p:
		return output'''
	
	# Non dominated sort
	nd_sort = [[output[0]]]

	for ind in range(1, len(output)):
		# Check whether the current test of output is added
		added = False

		for group in range(len(nd_sort)):
			# Deleted members which dominates or dominated by new test
			del_mem = []

			add_ind = -1
			group_ind = 0

			while group_ind < len(nd_sort[group]):
				mem = nd_sort[group][group_ind]
				dom_res = dom(output[ind][1], mem[1], leaf_index)
				
				# If new case dominates, add deleted ones after it
				if dom_res == 0:
					add_ind = group + 1
					del_mem.append(mem)
					del nd_sort[group][group_ind]

				# Non of members dominate each other
				# So two cases cannot happen at the same time
				elif dom_res == 1:
					add_ind = group
					del_mem.append(mem)
					del nd_sort[group][group_ind]

				else:
					group_ind += 1

			# New case is dominated by whole group
			if add_ind == group and not nd_sort[group]:
				nd_sort[group] = del_mem
				continue

			else:
				nd_sort[group].append(output[ind])
				added = True
				
				if add_ind != -1:
					nd_sort.insert(add_ind, del_mem)
				
				break

		# If new test is dominated by all
		if not added:
			nd_sort.append([output[ind]])
	
	# List of 
	rt = []

	for group in nd_sort:
		if len(group) <= p:
			rt.extend(group)
			p -= len(group)
		
		else:
			rt.extend(crowd_sel(group, p))
			break


	return nd_sort



# Mutate given input
def mutate(output):
	print('mutate', output)
	change = 0

	for ind in range(len(output)):
		if rand.random() <= 0.1:
			output[ind] -= 1
			change +=1

		elif rand.random() <= 0.2:
			output[ind] += 1
			change += 1
	
	# If none is changed, muteate again
	if change == 0:
		return mutate(output)
	
	return output

pop_sel([([], {0: 1, 1: 1}), ([], {0: 0, 1: 2}), ([], {0: 1, 1: 2}), ([], {0: 2 , 1: 2}), ([], {0: -1, 1: -1})], [0, 1], 2)
