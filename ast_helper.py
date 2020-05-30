import ast
import astor

# Find ast.Num node
def find_num(node):
	if isinstance(node, ast.Num):
		return [node.n]
	
	if isinstance(node, ast.Return):
		return []
	
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
# 0(==), 1(<), 2(<=, >=), 3(<. >)
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
		return 3, ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])

	elif isinstance(test.ops[0], ast.LtE):
		return 2, ast.BinOp(left=test.left, op=ast.Sub(), right=test.comparators[0])
	
	elif isinstance(test.ops[0], ast.Gt):
		return 3, ast.BinOp(left=test.comparators[0], op=ast.Sub(), right=test.left)

	elif isinstance(test.ops[0], ast.GtE):
		return 2, ast.BinOp(left=test.comparators[0], op=ast.Sub(), right=test.left)


class branch:
	br_list = [None]
	
	# parent: index of parent, op_type:
	def __init__(self, parent, op_type, lineno):
		self.ind = len(branch.br_list)

		# Ind of parent(if on true branch positive, elsewise negative)
		self.parent = parent
		self.op_type = op_type
		
		# Wheter it has child on true, false branch
		self.true = False
		self.false = False
		
		# Add itself to parent's branch
		if parent > 0:
			branch.br_list[parent].true = True
		elif parent < 0:
			branch.br_list[-parent].false = True

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

					# Assign branch distance to temporary variable
					body.insert(ind, ast.Assign(targets=[ast.Name(id=temp_name)],
												value=node))

					# Print branch_id, op_type, branch distance in order
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
					find_if(line.orelse, -new_branch.ind, temp_name, file_name)
					ind += 2

				else:
					find_if(line, parent, temp_name, file_name)
				ind += 1
