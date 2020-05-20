import ast
import astor
import random as rand
import sys

# Find constant number of code
def find_num(node):
    if isinstance(node, ast.Num):
        return [node.n]

    rt = []

    try:
        for value in node.__dict__.values():
            rt.extend(find_num(value))
    except AttributeError:
        if isinstance(node, list):
            for item in node:
                rt.extend(find_num(item))

    return rt


# Find string of code
def find_str(node):
    if isinstance(node, ast.Str):
        return [node.s]

    rt = []

    try:
        for value in node.__dict__.values():
            rt.extend(find_str(value))
    except AttributeError:
        if isinstance(node, list):
            for item in node:
                rt.extend(find_str(item))

    return rt


# Find branch of code from function body ast
def find_if(body):
    for stmt in body:
        if isinstance(stmt, ast.If):
            print(astor.dump_tree(stmt))
            find_if(stmt.orelse)


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
    func.body.insert(0, ast.Assign(targets=[ast.Name(id='b')], value=ast.Num(n=3)))
    code = astor.to_source(root)
    source_file = open('test.py', 'w')
    source_file.write(code)
    
    print(find_str(func))
    find_if(func.body)
    gen_input(func, 10)
