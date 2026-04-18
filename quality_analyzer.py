# import ast
# import re
# def analyze_quality(code):
#     try:
#         tree = ast.parse(code)
#         complexity = 1
#         nesting = 0
#         max_nesting = 0
#         issues = 0

#         for node in ast.walk(tree):
#             if isinstance(node, (ast.If, ast.For, ast.While)):
#                 complexity += 1
#                 nesting += 1
#                 max_nesting = max(max_nesting, nesting)

#         # Naming issues
#         naming_issues = []

#         for node in ast.walk(tree):
#             if isinstance(node, ast.FunctionDef):
#                 if not re.match(r'^[a-z_]+$', node.name):
#                     naming_issues.append(f"Function '{node.name}' should be snake_case")

#             if isinstance(node, ast.Name):
#                 if len(node.id) == 1 and node.id not in ["i", "j", "k"]:
#                     naming_issues.append(f"Variable '{node.id}' name is too short")

#         naming_issues = list(set(naming_issues))
#         issues = len(naming_issues)

#         score = 20
#         score -= min(complexity, 5)
#         score -= min(max_nesting, 3)
#         score -= issues

#         if score >= 15:
#             rating = "Excellent"
#         elif score >= 10:
#             rating = "Good"
#         else:
#             rating = "Needs Improvement"

#         return {
#             "score": f"{score}/20",
#             "rating": rating,
#             "cyclomatic_complexity": complexity,
#             "max_nesting": max_nesting,
#             "maintainability_issues": naming_issues,
#             "issues_detected": issues
#         }

#     except Exception:
#         return {
#             "score": "0/20",
#             "rating": "Invalid Code",
#             "cyclomatic_complexity": 0,
#             "max_nesting": 0,
#             "maintainability_issues": ["Invalid Python code"],
#             "issues_detected": 1
#         }

import ast
import math
import re
def analyze_quality(code):
    try:
        tree = ast.parse(code)
        loc = len(code.splitlines())
        complexity = 1
        operators = 0
        operands = 0
        unique_tokens = set()
        smells = []
        for node in ast.walk(tree):
            # Cyclomatic complexity
            if isinstance(node, (ast.If, ast.For, ast.While, ast.And, ast.Or, ast.ExceptHandler)):
                complexity += 1
            # Operators (rough)
            if isinstance(node, (ast.BinOp, ast.BoolOp, ast.Compare)):
                operators += 1
                unique_tokens.add(type(node).__name__)
            # Operands
            if isinstance(node, ast.Name):
                operands += 1
                unique_tokens.add(node.id)
            # Function length
            if isinstance(node, ast.FunctionDef):
                length = len(node.body)
                if length > 50:
                    smells.append(f"Function '{node.name}' is too long")
                # Too many arguments
                if len(node.args.args) > 5:
                    smells.append(f"Function '{node.name}' has too many parameters")
                # Naming
                if not re.match(r'^[a-z_]+$', node.name):
                    smells.append(f"Function '{node.name}' should be snake_case")
        # Halstead Volume (approx)
        N = operators + operands
        n = len(unique_tokens) if unique_tokens else 1
        volume = N * math.log2(n) if n > 1 else 0
        # Maintainability Index
        if loc > 0 and volume > 0:
            mi = 171 - 5.2 * math.log(volume) - 0.23 * complexity - 16.2 * math.log(loc)
            mi = max(0, min(100, mi))
        else:
            mi = 100
        # Rating
        if mi >= 85:
            rating = "Highly Maintainable"
        elif mi >= 65:
            rating = "Moderate Maintainability"
        else:
            rating = "Low Maintainability"
        return {
            "loc": loc,
            "cyclomatic_complexity": complexity,
            "halstead_volume": round(volume, 2),
            "maintainability_index": round(mi, 2),
            "rating": rating,
            "code_smells": list(set(smells)),
            "smell_count": len(smells)
        }

    except:
        return {
            "maintainability_index": 0,
            "rating": "Invalid Code",
            "code_smells": ["Invalid Python code"]
        }
    
sample_code = """
import math

def BadFunctionName(a, b, c, d, e, f):
    x = 0
    y = 1
    z = 2

    for i in range(10):
        if i % 2 == 0 and i > 5:
            x = x + i
        else:
            x = x - i

    while x < 100:
        if x % 3 == 0:
            x += 3
        elif x % 5 == 0:
            x += 5
        else:
            x += 1

    try:
        result = a + b * c - d / e
    except Exception:
        result = 0

    return result


def small():
    a = 1
    b = 2
    return a + b
"""
if __name__ == "__main__":
    result = analyze_quality(sample_code)

    print("Code Quality Analysis:\n")
    for key, value in result.items():
        print(f"{key}: {value}")