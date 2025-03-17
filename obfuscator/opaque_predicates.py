import ast
import random

class OpaquePredicateInjector(ast.NodeTransformer):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def opaque_condition(self):
        # Create an expression that always evaluates to False.
        # For example: ((3 * 7) - 21) > 0  is always False.
        expr = ast.Compare(
            left=ast.BinOp(
                left=ast.BinOp(
                    left=ast.Constant(value=3),
                    op=ast.Mult(),
                    right=ast.Constant(value=7)
                ),
                op=ast.Sub(),
                right=ast.Constant(value=21)
            ),
            ops=[ast.Gt()],
            comparators=[ast.Constant(value=0)]
        )
        return expr

    def visit_FunctionDef(self, node):
        # Insert an opaque predicate at a random position in the function body.
        if not node.body:
            return node
        
        opaque_if = ast.If(
            test=self.opaque_condition(),
            body=[
                ast.Expr(
                    value=ast.Call(
                        func=ast.Name(id="print", ctx=ast.Load()),
                        args=[ast.Constant(value="Dead opaque code")],
                        keywords=[]
                    )
                )
            ],
            orelse=[]
        )
        pos = random.randint(0, len(node.body))
        node.body.insert(pos, opaque_if)
        if self.verbose:
            print(f"Inserted opaque predicate in function {node.name} at position {pos}")
        return self.generic_visit(node)

def inject_opaque_predicates(tree, verbose=False):
    injector = OpaquePredicateInjector(verbose)
    return injector.visit(tree)
