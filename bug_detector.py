# import ast

# def detect_issues(code):
#     try:
#         tree = ast.parse(code)
#         issues = []

#         class Analyzer(ast.NodeVisitor):

#             def visit_FunctionDef(self, node):
#                 # ❌ Ignore __init__
#                 if node.name == "__init__":
#                     return

#                 has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))

#                 # ❌ Only warn if function is NOT recursive + no return
#                 is_recursive = any(
#                     isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == node.name
#                     for n in ast.walk(node)
#                 )

#                 if not has_return and not is_recursive:
#                     issues.append(f"Function '{node.name}' has no return statement")

#                 self.generic_visit(node)

#         Analyzer().visit(tree)

#         return issues

#     except:
#         return ["Invalid Python code"]

import ast
def detect_issues(code):
    try:
        tree = ast.parse(code)
        issues = []

        class Analyzer(ast.NodeVisitor):
            def __init__(self):
                self.functions = set()
            def visit_FunctionDef(self, node):
                # Duplicate function check
                if node.name in self.functions:
                    issues.append(f"Duplicate function '{node.name}'")
                self.functions.add(node.name)
                # Check return usage
                has_return = any(isinstance(n, ast.Return) for n in ast.walk(node))
                is_recursive = any(
                    isinstance(n, ast.Call) and isinstance(n.func, ast.Name) and n.func.id == node.name
                    for n in ast.walk(node)
                )
                if node.name == "__init__":
                    # __init__ should not return value
                    for n in ast.walk(node):
                        if isinstance(n, ast.Return) and n.value is not None:
                            issues.append("__init__ should not return a value")
                else:
                    if not has_return and not is_recursive:
                        issues.append(f"Function '{node.name}' has no return statement")
                # Too many arguments
                if len(node.args.args) > 5:
                    issues.append(f"Function '{node.name}' has too many arguments")
                # Missing docstring
                if not ast.get_docstring(node):
                    issues.append(f"Function '{node.name}' has no docstring")
                self.generic_visit(node)
            def visit_Return(self, node):
                # Unreachable code after return
                parent = getattr(node, 'parent', None)
                if parent and hasattr(parent, 'body'):
                    idx = parent.body.index(node)
                    if idx < len(parent.body) - 1:
                        issues.append("Unreachable code detected after return")
                self.generic_visit(node)
            def visit_Call(self, node):
                # Detect eval/exec usage
                if isinstance(node.func, ast.Name):
                    if node.func.id in ['eval', 'exec']:
                        issues.append(f"Use of dangerous function '{node.func.id}'")
                self.generic_visit(node)
        # Attach parent references (needed for unreachable detection)
        for node in ast.walk(tree):
            for child in ast.iter_child_nodes(node):
                child.parent = node
        Analyzer().visit(tree)
        return issues
    except:
        return ["Invalid Python code"]
    
if __name__ == "__main__":
    sample_code = """
def foo(a, b, c, d, e, f):
    x = 10

def foo(x):
    return x
    print("This is unreachable")

class Test:
    def __init__(self):
        return 5

def bar():
    eval("2+2")
"""

    result = detect_issues(sample_code)

    print("Issues Detected:")
    for issue in result:
        print("-", issue)