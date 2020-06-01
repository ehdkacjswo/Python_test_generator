import ast, astor
import sys, os, copy, math, argparse, imp, importlib
import random as rand
from ast_helper import find_num, find_if, name_len, branch
from ga_helper import mutate, in_test, add_test

# Generarte input from function ast
def gen_input(func):
	rt = []
	arg_num = len(func.args.args)
	special = list(set(find_num(func.body) + [0, 1, -1]))
	
	while len(rt) < p:
		inp = []
		
		for j in range(arg_num):
			if rand.random() <= 0.2:
				inp.append(rand.choice(special))
			else:
				inp.append(rand.randint(-100, 100))
		
		rt = add_test(rt, inp)

	return special, rt


# Analyze the fitness output
def get_result(leaf_index):
	f = open(br_file, "r")
	br_data = f.readlines()
	f.close()

	# Maps branch id to branch distance
	# Positive id : true branch, Negative id : false branch
	# Passed branches : negative distance
	br_dict = {}

	for data in br_data:
		br_id, br_type, br_dist = [int(x) for x in data.split(" ")]
		
		# When branch is passed, make fitness negative(-1)
		if (br_type == 0 and br_dist <= 0) or (br_type == 1 and br_dist < 0):
			new_data = [(br_id, -1), (-br_id, -br_dist)]
		else:
			new_data = [(br_id, br_dist), (-br_id, -1)]

		for tup in new_data:
			item = br_dict.get(tup[0])

			if item is None or item > tup[1]:
				br_dict[tup[0]] = tup[1]
		
	br_fit = {}

	# For each leaves, find fitness
	for leaf_ind, lvl_dict in leaf_index.items():
		for ind, lvl in sorted(lvl_dict.items(), key=lambda tup: tup[1]):
			dist = br_dict.get(ind)

			if dist is not None:
				if dist >= 0:
					br_fit[leaf_ind] = lvl + float(dist + 1) / (dist + 2)
					break

				if dist < 0:
					if lvl == 0:
						br_fit[leaf_ind] = -1

					# Parent passed but did not reach its child
					else:
						br_fit[leaf_ind] = lvl
					
					break
		
		# None itself or ancestors visited
		if not leaf_ind in br_fit:
			br_fit[leaf_ind] = len(lvl_dict) + 1

	return br_fit

# Helps to suppress print
class HiddenPrint:
	def __enter__(self):
		self._original_stdout = sys.stdout
		sys.stdout = open(os.devnull, 'w')
	
	def __exit__(self, exc_type, exc_val, exc_tb):
		sys.stdout.close()
		sys.stdout = self._original_stdout

# Return string that 
def tf_br(ind):
	return '{}{}'.format(abs(ind), 'T' if ind > 0 else 'F')

# Main part tests, evolves test cases
def test_main(root_copy, body_ind, func_file_name):
	func = root_copy.body[body_ind]

	if not isinstance(func, ast.FunctionDef):
		return

	func_name = func.name
	print('Function found ({})\n'.format(func_name))
	func.name = new_func_name

	if not func.args.args:
		return 

	branch.br_list = [None]
	find_if(func.body, 0, temp_name, file_name, True)
	
	print('{} branches found'.format(len(branch.br_list) - 1))
	
	# No branches found
	if len(branch.br_list) == 1:
		return
	
	for cur_br in branch.br_list[1:]:
		print('Branch #{} on line {}'.format(cur_br.ind, cur_br.lineno))

	# Generate input
	special, new_test = gen_input(func)	

	# Change function name and Import original function
	func.name = new_func_name
	root_copy.body.insert(0, ast.ImportFrom(module=sys.argv[1][:-3], names=[ast.alias(name=func_name, asname=None)], level=0))
	func.args.args.insert(0, ast.Name(id=file_name))

	# Write changed code on new file
	code = astor.to_source(root_copy)
	source_file = open(func_file_name, 'w')
	source_file.write(code)
	source_file.close()

	# Get index of leaf branches (ind, app_lvl)
	leaf_index = {}

	for cur_br in branch.br_list[1:]:
		# At least one of branches is leaf
		if cur_br.reach and ((not cur_br.true) or (not cur_br.false)):
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
	
	# Used for final printing
	leaf_index_copy = copy.deepcopy(leaf_index)
	
	# Branch fitness output with(test, output)
	output = {}

	# Print leaf branches and init output
	print('\nLeaf branches:')

	for leaf_ind in sorted(leaf_index.keys(), key=lambda ind: abs(ind) * 2 + (1 if ind < 0 else 0)):
		print('{} '.format(tf_br(leaf_ind))),
		output[leaf_ind] = []
	
	print('\n')
	
	# Import revised code
	module = importlib.import_module(func_file_name[:-3])
	method = getattr(module, new_func_name)
	
	# Tests that cover each leaves
	leaf_test = {}
	sol_found = False

	mid_gen = {int(math.floor(gen * i * 0.1)): i for i in range(1, 11)}

	for i in range(gen):
		if i in mid_gen:
			print('{}0% generation processed'.format(mid_gen[i]))

		new_output = []

		for inp in new_test:
			with HiddenPrint():
				with open(br_file, 'w') as br_report:
					try:
						method(br_report, *inp)
					except:
						#Do nothing
						i = i

			new_output.append((inp, get_result(leaf_index)))
				
			# Check whether the solution is found
			for leaf_ind in leaf_index:
				# When the test is found for leaf
				if new_output[-1][1][leaf_ind] < 0:
					leaf_test[leaf_ind] = copy.deepcopy(inp)
					del leaf_index[leaf_ind]
					
					if not bool(leaf_index):
						print('Every tests ares found!\n')
						sol_found = True
					break

			if sol_found:
				break

		# Solution found or last generation
		if sol_found or i == gen - 1:
			break
		
		new_test = []
		last_test_num = 0

		for leaf_ind in leaf_index:
			# Selct next generation saving some of current population
			output[leaf_ind].extend(new_output)
			output[leaf_ind] = output[leaf_ind][:save_p] + sorted(output[leaf_ind][save_p:], key=lambda data: data[1][leaf_ind])[:p - save_p]
			output[leaf_ind] = sorted(output[leaf_ind], key=lambda data: data[1][leaf_ind])

			# Generate test case until p tests
			while len(new_test) - last_test_num < p:
				pair = []
					
				# Binary tournament selection
				for k in range(2):
					p1 = rand.choice(output[leaf_ind])
					p2 = rand.choice(output[leaf_ind])

					if p1[1][leaf_ind] < p2[1][leaf_ind]:
						pair.append(p1)
					elif p1[1][leaf_ind] > p2[1][leaf_ind]:
						pair.append(p2)
					else:
						pair.append(rand.choice([p1, p2]))

				if pair[0][0] == pair[1][0]:
					continue

				score1 = pair[0][1][leaf_ind]
				score2 = pair[1][1][leaf_ind]

				children = []

				# Single point crossover
				if len(pair[0][0]) > 1:
					cross_point = rand.randint(1, len(pair[0][0]) - 1)

					children.append(pair[0][0][:cross_point] + pair[1][0][cross_point:])
					children.append(pair[1][0][:cross_point] + pair[0][0][cross_point:])

				# If single point crossover is unvailable, mutate
				else:
					children.append(mutate(pair[0][0], special, 1.0, alpha, beta))
					children.append(mutate(pair[1][0], special, 1.0, alpha, beta))
			
				# Secant method
				if score1 != score2:
					children.append([int(math.ceil((pair[0][0][k] * (score2 + 1) - pair[1][0][k] * (score1 + 1)) / (score2 - score1))) for k in range(len(pair[0][0]))])

				for child in children:
					if rand.random() < 0.2 or child == pair[0][0] or child == pair[1][0]:
						child = mutate(child, special, pm, alpha, beta)

					if not in_test([out[0] for out in output[leaf_ind]], child):
						new_test = add_test(new_test, child)

			last_test_num = len(new_test)
	
	node_test = {}

	for leaf_ind, lvl_dict in leaf_index_copy.items():
		# Solution found for leaf
		if leaf_ind in leaf_test:
			for parent in lvl_dict:
				node_test[parent] = leaf_test[leaf_ind]

		else:
			test = output[leaf_ind][0][0]
			best_lvl = int(math.ceil(output[leaf_ind][0][1][leaf_ind]))

			for parent, lvl in lvl_dict.items():
				# Add when only it's visited
				if lvl >= best_lvl:
					node_test[parent] = test
	
	for ind in range(1, len(branch.br_list)):
		tf = [ind, -ind]

		for br in tf:
			# Solution found
			if br in node_test:
				print('{}: {}'.format(tf_br(br), node_test[br]))
			# Solution not found
			else:
				print('{}: -'.format(tf_br(br)))

	print('\n')

	# Delete trashes
	del module
	del method

	if os.path.exists(func_file_name):
		os.remove(func_file_name)
	if os.path.exists(br_file):
		os.remove(br_file)

	return

if __name__ == "__main__":
	parser = argparse.ArgumentParser()
	parser.add_argument('py_file', type=str, help='Input python function file')
	parser.add_argument('-p', '--p', type=int, help='Number of population', default=100)
	parser.add_argument('-g', '--gen', type=int, help='Number of generation', default=1000)
	parser.add_argument('-pm', '--pm', type=int, help='Probability of mutation in percentage', default=20)
	parser.add_argument('-ps', '--ps', type=int, help='Percentage of population saved <= 50', default = 10)
	parser.add_argument('-a', '--alpha', type=int, help='Alpha of gamma distribution', default=1)
	parser.add_argument('-b', '--beta', type=int, help='Beta of gamma distribution', default=1)
	parser.add_argument('-f', '--func', type=str, help='Name of revised python file', default='branch_dist_print')
	parser.add_argument('-br', '--br', type=str, help='Name of branch distance file', default='br_dist')

	args = parser.parse_args()
	root = astor.code_to_ast.parse_file(args.py_file)
	
	# Apply not used variable name for output file and temp var
	var_len = name_len(root.body) + 1
	file_name = 'f' * var_len
	temp_name = 't' * var_len
	new_func_name = 'f' * (var_len + 1)

	# Size of population
	p = args.p if args.p > 0 else 100
	save_p = int(math.floor(float(p) * (args.ps if args.ps in range(0, 51) else 10) / 100))
	
	# Number of generations
	gen = args.gen if args.gen > 0 else 1000
	pm = args.pm if args.pm in range(0, 101) else 20
	pm = float(pm) / 100

	# Gamma distribution
	alpha = args.alpha if args.alpha > 0 else 1
	beta = args.beta if args.beta > 0 else 1
	
	# File names
	func_file = args.func
	br_file = args.br

	for ind in range(len(root.body)):
		test = test_main(copy.deepcopy(root), ind, func_file + str(ind) + '.py')
