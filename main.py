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

# Find ast.Name node
def find_name(node):
    if isinstance(node, ast.Name):
        return [node.id]
    
    rt = []
    
    try:
        for value in node.__dict__.values():
            rt.extend(find_name(value))
    except AttributeError:
        if isinstance(node, list):
            for child in node:
                rt.extend(find_name(child))

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
	def __init__(self, parent, op_type):
		self.ind = len(branch.br_list)
		self.parent = parent
		self.op_type = op_type
		self.child = 0

		branch.br_list.append(self)
		if parent != -1:
			branch.br_list[parent].child += 1


# Find branch of code from function body ast
def find_if(body, parent):
	try:
		if 'body' in body.__dict__:
			find_if(body.body, parent)
		if 'orelse' in body.__dict__:
			find_if(body.orelse, parent)

	except AttributeError:
		if isinstance(body, list):
			ind = 0

			while ind in range(len(body)):
				line = body[ind]

				if isinstance(line, ast.If):
					op_type, node = branch_dist(line.test)
					body.insert(ind, ast.Print(dest=None, values=[node], nl=True))
					new_branch = branch(parent, op_type)
					ind += 1

				find_if(line, parent)
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
	
	find_if(func.body, -1)
	
	print(astor.dump_tree(func))
	code = astor.to_source(root)
	source_file = open('branch_dist_print.py', 'w')
	source_file.write(code)
	print(find_name(func))
	gen_input(func, 10)
