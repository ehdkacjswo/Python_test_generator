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

# Comparators used for if statements
comp_op = [ast.Eq, ast.NotEq, ast.Lt, ast.LtE, ast.Gt, ast.GtE]

# Get branch distance for given if statement
def branch_dist(test):
	if isinstance(test.ops[0], ast.Eq):
		return ast.Call(func=ast.Name(id='abs'),
						args=[ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])],
						keywords=[],
						starags=None,
						kwargs=None)
	
	elif isinstance(test.ops[0], ast.NotEq):
		return ast.UnaryOp(op=ast.USub(),
							operand=ast.Call(func=ast.Name(id='abs'),
												args=[ast.BinOp(left=test.left, op=ast.Sub(),
														right=test.comparators[0])],
												keywords=[],
												starags=None,
												kwargs=None))
	
	elif isinstance(test.ops[0], ast.Lt) or isinstance(test.ops[0], ast.LtE):
		return ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])
	
	elif isinstance(test.ops[0], ast.Gt) or isinstance(test.ops[0], ast.GtE):
		return ast.BinOp(left=test.comparators[0], op=ast.Sub(), right=test.left)



# Find branch of code from function body ast
def find_if(body):
	body.insert(0, ast.Print(dest=None, values=[ast.Num(n=1)], nl=True))
	ind = 0

	while ind < len(body):
		line = body[ind]

		if isinstance(line, ast.If):
			body.insert(ind, ast.Print(dest=None,
										values=[branch_dist(line.test)],
										nl=True))
			find_if(line.orelse)
			ind += 1

		ind += 1



# Generarte input from function ast
def gen_input(func, num):
    rt = []
    leng = len(func.args.args)
    special = find_num(func.body)

    print(special)

    print(rand.random())
    

'''tree = astor.code_to_ast.parse_file("function.py")
tree = tree.body[1]
dump = astor.dump_tree(tree)
print(tree.args.args)
find_if(tree.body)

for ind, item in enumerate(tree.body):
    print(item.__dict__)
    if isinstance(item, ast.If):
        print(ind, item)

print(len(tree.args.args))
print(type(tree))
print(dump)'''

if __name__ == "__main__":
	root = astor.code_to_ast.parse_file(sys.argv[1])
	func = root.body[0]
	
	find_if(func.body)
	
	print(astor.dump_tree(func))
	func.body.insert(0, ast.Assign(targets=[ast.Name(id='b')], value=ast.Num(n=3)))
	code = astor.to_source(root)
	source_file = open('test.py', 'w')
	source_file.write(code)
	print(find_name(func))
	gen_input(func, 10)
