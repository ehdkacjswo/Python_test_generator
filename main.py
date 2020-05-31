import ast, astor
import sys, os, copy, math
import random as rand
from ast_helper import find_num, find_if, name_len, branch
from ga_helper import pop_sel, mutate

# Generarte input from function ast
def gen_input(func):
	rt = []
	arg_num = len(func.args.args)
	special = list(set(find_num(func.body) + [0, 1, -1]))
	
	for i in range(p):
		inp = []
		
		for j in range(arg_num):
			if rand.random() <= 0.2:
				inp.append(rand.choice(special))
			else:
				inp.append(rand.randint(-100, 100))
		
		rt.append(inp)

	return special, rt


# Analyze the fitness output
def get_result(lvl_dict):
	f = open("fitness", "r")
	br_data = f.readlines()
	f.close()

	# Maps branch id to branch distance
	# Positive id : true branch, Negative id : false branch
	# Passed branches : negative distance
	br_dict = {}

	for data in br_data:
		br_id, br_type, br_dist = [int(x) for x in data.split(" ")]
		
		# When branch is passed, make fitness negative
		if (br_type % 2 == 0 and br_dist <= 0) or (br_type % 2 == 1 and br_dist < 0):
			new_data = [(br_id, -1), (-br_id, -br_dist)]
		else:
			new_data = [(br_id, br_dist), (-br_id, -1)]

		for tup in new_data:
			item = br_dict.get(tup[0])

			if item is None or item > tup[1]:
				br_dict[tup[0]] = tup[1]
		
	cur_cov = len(lvl_dict) + 2

	# 
	for ind, lvl in sorted(lvl_dict.items(), key=lambda tup: tup[1]):
		dist = br_dict.get(ind)

		if dist is not None:
			if dist >= 0:
				br_cov = lvl + float(dist) / (dist + 1)
				break

			if dist < 0:
				if lvl == 0:
					br_cov = -1
					break
				else:
					# Cannot reach
					print('hello')
		
	return br_cov

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
def test_main(root_copy, body_ind):
	func = root_copy.body[body_ind]

	if not isinstance(func, ast.FunctionDef):
		return

	func_name = func.name
	out_res.write('Function found ({})\n'.format(func_name))
	special, new_test = gen_input(func)

	branch.br_list = [None]
	find_if(func.body, 0, temp_name, file_name)

	# Open file(branch fitness that will save fitness values
	func.body.insert(0, ast.Assign(targets=[ast.Name(id=file_name)],
									value=ast.Call(func=ast.Name(id='open'),
													args=[ast.Str(s='fitness'), ast.Str(s='w')],
													keywords=[],
													starargs=None,
													kwargs=None)))
	
	# Close file
	func.body.append(ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(id=file_name), attr='close'),
												args=[],
												keywords=[],
												starargs=None,
												kwargs=None)))

	out_res.write('{} branches found\n\n'.format(len(branch.br_list) - 1))
	
	# No branches found
	if len(branch.br_list) == 1:
		return
	
	for cur_br in branch.br_list[1:]:
		out_res.write('Branch #{} on line {}\n'.format(cur_br.ind, cur_br.lineno))

	# Write changed code on new file
	code = astor.to_source(root_copy)
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
	
	# Print leaf branches
	out_res.write('Leaf branches:')

	for leaf_ind in sorted(leaf_index.keys(), key=lambda ind: abs(ind) * 2 + (1 if ind < 0 else 0)):
		out_res.write(' {}'.format(tf_br(leaf_ind)))
	
	out_res.write('\n\n')
	
	import branch_dist_print
	method = getattr(branch_dist_print, func_name)
	
	# Branch fitness output with (test, output)
	output = []
	rt_test = {}
	
	for leaf_ind in leaf_index.keys():
		#Wheter the solution found
		sol_found = False

		print(leaf_ind)

		for i in range(gen):
			new_output = []

			for inp in new_test:
				with HiddenPrint():
					method(*inp)

				new_output.append((inp, get_result(leaf_index[leaf_ind])))
				
				# Check whether the solution is found
				if new_output[-1][1] < 0:
					sol_found = True
					rt_test[leaf_ind] = copy.deepcopy(inp)
					out_res.write('Test case for {} is found\n')
					break

			if sol_found:
				break

			output.extend(new_output)
			output = sorted(output, key=lambda data: data[1])[:p]
			print(output)

			new_test = []

			for j in range(p):
				pair = []
					
				for k in range(2):
					p1 = rand.choice(output)
					p2 = rand.choice(output)

					if p1[1] < p2[1]:
						pair.append(p1)
					elif p1[1] > p2[1]:
						pair.append(p2)
					else:
						pair.append(rand.choice([p1, p2]))

				score1 = pair[0][1]
				score2 = pair[1][1]
			
				if score1 == score2:
					new_test.append(mutate(pair[0][0], special))

				else:
					child = [int(math.ceil((pair[0][0][k] * (score2 + 1) - pair[1][0][k] * (score1 + 1)) / (score2 - score1))) for k in range(len(pair[0][0]))]

					if rand.random() <= 0.2:
						child = mutate(child, special)

					new_test.append(child)
	

	print(rt_test)
	print(leaf_index.keys())
	return rt_test

if __name__ == "__main__":
	root = astor.code_to_ast.parse_file(sys.argv[1])
	print(astor.dump_tree(root))
	
	# Apply not used variable name for output file and temp var
	var_len = name_len(root) + 1
	file_name = 'f' * var_len
	temp_name = 't' * var_len
	
	out_res = open('branch_test', 'w')

	p = 10
	gen = 1000
	
	for ind in range(len(root.body)):
		test_main(copy.deepcopy(root), ind)
	
