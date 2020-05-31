import numpy as np
import random as rand

def crowd_sel(group, leaf_index, p):
	if p == 0:
		return []
	
	# (index of original group, crowd distance, number of inf)
	ind_group = [[i, 0, 0] for i in range(len(group))]
	
	for leaf_ind in leaf_index:
		ind_group.sort(key=lambda test: group[test[0]][1][leaf_ind])

		# Set infinite
		ind_group[0][2] += 1
		ind_group[-1][2] += 1

		for i in range(1, len(ind_group) - 1):
			# Crowding distance
			ind_group[i][1] += group[ind_group[i + 1][0]][1][leaf_ind] - group[ind_group[i - 1][0]][1][leaf_ind]
	
	ind_group.sort(key=lambda crowd: crowd[2] + crowd[1] / (crowd[1] + 1), reverse=True)
	
	rt = []
	for i in range(p):
		rt.append(group[ind_group[i][0]])
	
	return rt

# 0: test1 dominates, 1: test2 dominates, 2: non-dominating
def dom(test1, test2, leaf_index):
	# Whether test1 or test2 dominates
	dom1 = False
	dom2 = False

	for leaf_ind in leaf_index:
		if test1[leaf_ind] > test2[leaf_ind]:
			dom2 = True
		elif test2[leaf_ind] > test1[leaf_ind]:
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
			rt.extend(crowd_sel(group, leaf_index, p))
			break

	return rt


# Mutate given input
def mutate(output):
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
