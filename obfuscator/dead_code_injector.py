import ast
import random

class DeadCodeInjector(ast.NodeTransformer):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def inject_in_function(self, node):
        # Create a dead code statement, e.g., a dummy print.
        dead_str = "deadcode_" + str(random.randint(1000, 9999))
        dead_code = ast.Expr(
            value=ast.Call(
                func=ast.Name(id="print", ctx=ast.Load()),
                args=[ast.Constant(value=dead_str)],
                keywords=[],
            )
        )
        if self.verbose:
            print(f"Injecting dead code in function: {node.name}")
        node.body.insert(0, dead_code)
        return node

    def visit_FunctionDef(self, node):
        node = self.inject_in_function(node)
        self.generic_visit(node)
        return node

def inject_dead_code(tree, verbose=False):
    injector = DeadCodeInjector(verbose)
    return injector.visit(tree)
