import ast
import astor
import random as rand
import sys
import copy
from ast_helper import find_num, find_if, name_len, branch
from ga_helper import pop_sel, mutate

# Generarte input from function ast
def gen_input(func):
	rt = []
	arg_num = len(func.args.args)
	special = list(set(find_num(func.body).extend([0, 1, -1])))
	
	for i in range(p):
		inp = []
		
		for j in range(arg_num):
			if rand.random() <= 0.2:
				inp.append(rand.choice(special))
			else:
				inp.append(rand.randint(-10000, 10000))
		
		rt.append(inp)

	return rt


# Analyze the fitness output
def get_result(leaf_index):
	f = open("fitness", "r")
	br_data = f.readlines()

	# Maps branch id to branch distance
	# Positive id : true branch, Negative id : false branch
	# Passed branches : negative distance
	br_dict = {}

	for data in br_data:
		br_id, br_type, br_dist = [int(x) for x in data.split(" ")]

		# For Eq and NotEq, don't normalize
		if br_type < 2:
			if (br_type == 0 and br_dist <= 0) or (br_type == 1 and br_dist < 0):
				new_data = [(br_id, -1), (-br_id, -br_dist)]
			else:
				new_data = [(br_id, br_dist), (-br_id, -1)]
			
		# For others, nomarlize the distance
		else:
			if (br_type % 2 == 0 and br_dist <= 0) or (br_type % 2 == 1 and br_dist < 0):
				new_data = [(br_id, -1), (-br_id, -br_dist + k)]
			else:
				new_data = [(br_id, br_dist + k), (-br_id, -1)]

		for tup in new_data:
			item = br_dict.get(tup[0])

			if item is None or item > tup[1]:
				br_dict[tup[0]] = tup[1]
		
	# Branch coverage for every leaves
	br_cov = {}

	for leaf_ind, lvl_dict in leaf_index.items():
		cur_cov = len(lvl_dict) + 2

		# 
		for ind, lvl in sorted(lvl_dict.items(), key=lambda tup: tup[1]):
			dist = br_dict.get(ind)

			if dist is not None:
				if dist >= 0:
					br_cov[leaf_ind] = lvl + dist / (dist + 1)
					break

				if dist < 0:
					if lvl == 0:
						br_cov[leaf_ind] = -1
						break
					else:
						# Cannot reach
						print('hello')
		
	return br_cov

# Main part tests, evolves test cases
def test_main(root, ind):
	func = root.body[ind]

	if not isinstance(func, ast.FunctionDef):
		return

	func_name = func.name

	#gen_input(func)

	# Open file(branch fitness that will save fitness values
	func.body.insert(0, ast.Assign(targets=[ast.Name(id=file_name)],
									value=ast.Call(func=ast.Name(id='open'),
													args=[ast.Str(s='fitness'), ast.Str(s='w')],
													keywords=[],
													starargs=None,
													kwargs=None)))

	find_if(func.body, 0, temp_name, file_name)

	# Write changed code on new file
	code = astor.to_source(root)
	source_file = open('branch_dist_print.py', 'w')
	source_file.write(code)
	source_file.close()

	# Get index of leaf branches (ind, app_lvl)
	leaf_index = {}

	for cur_br in branch.br_list[1:]:
		# At least one of branches is leaf
		if (not cur_br.true) or (not cur_br.false):
			app_lvl = 1
			lvl_dict = {}
			next_ind = cur_br.parent

			# Add parents till the root
			while next_ind != 0:
				lvl_dict[next_ind] = app_lvl
				app_lvl += 1
				next_ind = branch.br_list[abs(next_ind)].parent

			# Branch without child branch is leaf
			if not cur_br.true:
				pos_dict = copy.deepcopy(lvl_dict)
				pos_dict[cur_br.ind] = 0
				leaf_index[cur_br.ind] = pos_dict
			if not cur_br.false:
				neg_dict = copy.deepcopy(lvl_dict)
				neg_dict[-cur_br.ind] = 0
				leaf_index[-cur_br.ind] = neg_dict
	
	import branch_dist_print
	method = getattr(branch_dist_print, func_name)
	
	# Branch fitness output with (test, output)
	output = []

	# New test cases and outputs generated
	new_test = [[3, 2, 3], [1, 2, 3], [3, 2, 1], [0, 0, 0]]
	new_output = []
	rt_test = {}
	
	for i in range(gen):
		for inp in new_test:
			method(*inp)
			new_output.append((inp, get_result(leaf_index)))

		# Look for leaf node that answer is found
		for res in new_output:
			for key, value in res[1].items():
				if value < 0 and (key in leaf_index):
					del leaf_index[key]
					rt_test[key] = copy.deepcopy(res[0])

					# Every leaves has solution
					if not bool(leaf_index):
						return rt_test

		output.extend(new_output)
		print(output, leaf_index.keys())
		output = pop_sel(output, leaf_index.keys(), 1)

		for j in range(p):
			# Index of leaf to optimize
			leaf_ind = rand.choice(leaf_index.keys())
			pair = []
				
			for k in range(2):
				p1 = rand.choice(output)
				p2 = rand.choice(output)

				if p1[1][leaf_ind] < p2[1][leaf_ind]:
					pair.append(p1)
				elif p1[1][leaf_ind] > p2[1][leaf_ind]:
					pair.append(p2)
				else:
					pair.append(rand.choice([p1, p2]))

			score1 = pair[0][1][leaf_ind]
			score2 = pair[1][1][leaf_ind]
			
			if score1 == score2:
				new_test.append(mutate(pair[0][0]))

			else:
				child = [math.ceil((pair[0][0][ind] * (score2 + 1) - pair[1][0][ind] * (score1 + 1)) / (score2 - score1))
							for l in range(len(pair[0][0]))]

				if rand.random() <= 0.2:
					child = mutate(child)

				new_test.append(child)

	return rt_test

if __name__ == "__main__":
	root = astor.code_to_ast.parse_file(sys.argv[1])
	
	# Apply not used variable name for output file and temp var
	var_len = name_len(root) + 1
	file_name = 'f' * var_len
	temp_name = 't' * var_len

	p = 10
	k = 1
	gen = 1000
	test_main(root, 0)
	
