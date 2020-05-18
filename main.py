import ast
import astor


# Find constant number of code
def find_num(node):
    if isinstance(node, ast.Num):
        return [node.n]

    rt = []

    try:
        for attr, value in node.__dict__.iteritems():
            rt.extend(find_num(value))
    except AttributeError:
        if isinstance(node, list):
            for item in node:
                rt.extend(find_num(item))

    return rt


# Find branch of code
def find_if(node):
    for stmt in enumerate(node):
        if isinstance(stmt, ast.If):
            cur = stmt
            while true:
                print(cur)
                cur = cur.orelse

tree = astor.code_to_ast.parse_file("function.py")
tree = tree.body[1]
dump = astor.dump_tree(tree)

print(find_num(tree))
find_if(tree.body)

for ind, item in enumerate(tree.body):
    print(item.__dict__)
    if isinstance(item, ast.If):
        print(ind, item)

print(len(tree.args.args))
print(type(tree))
print(dump)
