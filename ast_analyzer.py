import ast
def parse_code_structure(code):
    try:
        tree = ast.parse(code)
        functions = []
        classes = []
        imports = []
        loops = []

        for node in ast.walk(tree):
            if isinstance(node, ast.FunctionDef):
                functions.append(node.name)
            elif isinstance(node, ast.ClassDef):
                classes.append(node.name)
            elif isinstance(node, ast.Import):
                for n in node.names:
                    imports.append(n.name)
            elif isinstance(node, ast.ImportFrom):
                imports.append(node.module)
            elif isinstance(node, ast.For):
                loops.append("for loop")
            elif isinstance(node, ast.While):
                loops.append("while loop")

        return {
            "functions": functions,
            "classes": classes,
            "imports": imports,
            "loops": loops
        }
    except Exception:
        return {
            "functions": [],
            "classes": [],
            "imports": [],
            "loops": []
        }
    
# if __name__ == "__main__":
#     sample_code = """
# import os

# class Test:
#     def method(self):
#         for i in range(5):
#             print(i)

# def func():
#     while True:
#         break
#     """

# result = parse_code_structure(sample_code)
# print(result)