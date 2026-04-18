import ast
import numpy as np
import matplotlib.pyplot as plt


def analyze_complexity(code):
    try:
        tree = ast.parse(code)

        class Analyzer(ast.NodeVisitor):
            def __init__(self):
                self.depth = 0
                self.max_depth = 0
                self.recursion = False
                self.recursive_calls = 0
            def visit_For(self, node):
                self.depth += 1
                self.max_depth = max(self.max_depth, self.depth)
                self.generic_visit(node)
                self.depth -= 1
            def visit_While(self, node):
                self.depth += 1
                self.max_depth = max(self.max_depth, self.depth)
                self.generic_visit(node)
                self.depth -= 1
            def visit_FunctionDef(self, node):
                for n in ast.walk(node):
                    if isinstance(n, ast.Call) and isinstance(n.func, ast.Name):
                        if n.func.id == node.name:
                            self.recursion = True
                            self.recursive_calls += 1
                self.generic_visit(node)
        analyzer = Analyzer()
        analyzer.visit(tree)
        # -------- TIME COMPLEXITY --------
        if analyzer.recursion:
            if analyzer.recursive_calls == 1:
                time = "O(n)"
                explanation = "Linear recursion detected"
            elif analyzer.recursive_calls == 2:
                time = "O(2^n)"
                explanation = "Binary recursion detected (e.g., Fibonacci)"
            else:
                time = "O(k^n)"
                explanation = "Multiple recursive calls → exponential growth"
        else:
            if analyzer.max_depth == 0:
                time = "O(1)"
                explanation = "No loops detected → constant time"
            elif analyzer.max_depth == 1:
                time = "O(n)"
                explanation = "Single loop detected → linear time"
            else:
                time = f"O(n^{analyzer.max_depth})"
                explanation = f"{analyzer.max_depth} nested loops → polynomial complexity"

        # -------- SPACE COMPLEXITY --------
        if analyzer.recursion:
            space = "O(n)"
        elif analyzer.max_depth > 1:
            space = "O(n)"
        else:
            space = "O(1)"

        return {
            "time_complexity": time,
            "space_complexity": space,
            "explanation": explanation,
            "depth": analyzer.max_depth,
            "valid": True
        }

    except:
        return {
            "time_complexity": "Error",
            "space_complexity": "Error",
            "explanation": "Invalid Python code",
            "valid": False
        }


# -------- GRAPH GENERATOR --------
def plot_complexity_graph(time_complexity, space_complexity):
    n = np.linspace(1, 30, 100)

    def get_curve(c):
        if "O(1)" in c:
            return np.ones_like(n)
        elif "n^2" in c:
            return n**2
        elif "n^3" in c:
            return n**3
        elif "2^n" in c:
            return 2**(n / 5)
        elif "n" in c:
            return n
        else:
            return n

    fig, ax = plt.subplots(1, 2, figsize=(3.5, 1.5))

    ax[0].plot(n, get_curve(time_complexity))
    ax[0].set_title("Time", fontsize=10)
    ax[0].tick_params(labelsize=8)
    ax[0].grid(alpha=0.3)

    ax[1].plot(n, get_curve(space_complexity))
    ax[1].set_title("Space", fontsize=10)
    ax[1].tick_params(labelsize=8)
    ax[1].grid(alpha=0.3)

    plt.tight_layout(pad=0.5)

    return fig

