import ast
import astor
import random as rand
import sys

# Find ast.Num node
def find_num(node):
    if isinstance(node, ast.Num):
        return [node.n]

    rt = []

    try:
        for value in node.__dict__.values():
            rt.extend(find_num(value))
    except AttributeError:
        if isinstance(node, list):
            for child in node:
                rt.extend(find_num(child))

    return rt

# Maximum length of names
def name_len(node):
    if isinstance(node, ast.Name):
        return len(node.id)
    
    rt = 0
    
    try:
        for value in node.__dict__.values():
            rt = max(rt, name_len(value))
    except AttributeError:
        if isinstance(node, list):
            for child in node:
                rt = max(rt, name_len(child))

    return rt


# Get branch distance for given if statement
# 0(==), 1(<), 2(+K<), 3(+k<=)
def branch_dist(test):
	if isinstance(test.ops[0], ast.Eq):
		return 0, ast.Call(func=ast.Name(id='abs'),
							args=[ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])],
							keywords=[],
							starags=None,
							kwargs=None)
	
	elif isinstance(test.ops[0], ast.NotEq):
		return 1, ast.UnaryOp(op=ast.USub(),
								operand=ast.Call(func=ast.Name(id='abs'),
													args=[ast.BinOp(left=test.left, op=ast.Sub(),
															right=test.comparators[0])],
													keywords=[],
													starags=None,
													kwargs=None))
	
	elif isinstance(test.ops[0], ast.Lt):
		return 2, ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])

	elif isinstance(test.ops[0], ast.LtE):
		return 3, ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])
	
	elif isinstance(test.ops[0], ast.Gt):
		return 2, ast.BinOp(left=test.comparators[0], op=ast.Sub(), right=test.left)

	elif isinstance(test.ops[0], ast.GtE):
		return 3, ast.BinOp(left=test.comparators[0], op=ast.Sub(), right=test.left)


class branch:
	br_list = []
	
	# parent: index of parent, op_type:
	def __init__(self, parent, op_type, lineno):
		self.ind = len(branch.br_list)
		self.parent = parent
		self.op_type = op_type
		self.lineno = lineno

		branch.br_list.append(self)


# Find branch of code from function body ast
def find_if(body, parent, temp_name, file_name):
	try:
		if 'body' in body.__dict__:
			find_if(body.body, parent, temp_name, file_name)
		'''if 'orelse' in body.__dict__:
			find_if(body.orelse, parent)'''

	except AttributeError:
		if isinstance(body, list):
			ind = 0

			while ind in range(len(body)):
				line = body[ind]

				if isinstance(line, ast.If):
					op_type, node = branch_dist(line.test)
					new_branch = branch(parent, op_type, line.lineno)

					body.insert(ind, ast.Assign(targets=[ast.Name(id=temp_name)],
												value=node))

					body.insert(ind + 1, ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(id=file_name),
																					attr='write'),
													args=[ast.Call(func=ast.Attribute(value=ast.Str(s='{} {} {}\n'),
																						attr='format'),
																	args=[ast.Num(n=new_branch.ind),
																			ast.Num(n=op_type),
																			ast.Name(id=temp_name)],
																	keywords=[],
																	starargs=None,
																	kwargs=None)],
													keywords=[],
													starargs=None,
													kwargs=None)))

					find_if(line.body, new_branch.ind, temp_name, file_name)
					find_if(line.orelse, parent, temp_name, file_name)
					#new_branch = branch(parent, op_type)
					ind += 2

				else:
					find_if(line, parent, temp_name, file_name)
				ind += 1



# Generarte input from function ast
def gen_input(func, num):
    rt = []
    leng = len(func.args.args)
    special = find_num(func.body)

    print(special)

    print(rand.random())
    

if __name__ == "__main__":
	root = astor.code_to_ast.parse_file(sys.argv[1])
	func = root.body[0]
	
	# Apply not used variable name for output file and temp var
	var_len = name_len(root) + 1
	file_name = 'f' * var_len
	temp_name = 't' * var_len
	
	# Open file(branch fitness that will save fitness values
	func.body.insert(0, ast.Assign(targets=[ast.Name(id=file_name)],
									value=ast.Call(func=ast.Name(id='open'),
													args=[ast.Str(s='fitness'), ast.Str(s='w')],
													keywords=[],
													starargs=None,
													kwargs=None)))
	
	# Blueprint for writing fitness value
	# Only need to change write_func.args
	write_func = ast.Expr(value=ast.Call(func=ast.Attribute(value=ast.Name(id=file_name), attr='write'),
											args=[ast.Str(s='example')],
											keywords=[],
											starargs=None,
											kwargs=None))

	find_if(func.body, -1, temp_name, file_name)
	
	print(astor.dump_tree(func))
	code = astor.to_source(root)
	source_file = open('branch_dist_print.py', 'w')
	source_file.write(code)
	
	from branch_dist_print import *

	gen_input(func, 10)
