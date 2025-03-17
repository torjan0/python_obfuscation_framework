import ast

class ControlFlowFlattener(ast.NodeTransformer):
    def __init__(self, verbose=False):
        self.verbose = verbose

    def flatten_function(self, node):
        if not node.body:
            return node

        new_body = []
        # Initialize a state variable.
        state_init = ast.Assign(
            targets=[ast.Name(id="__state", ctx=ast.Store())],
            value=ast.Constant(value=0),
        )
        new_body.append(state_init)

        loop_body = []
        # Build a series of if-statements corresponding to each original statement.
        for idx, stmt in enumerate(node.body):
            condition = ast.Compare(
                left=ast.Name(id="__state", ctx=ast.Load()),
                ops=[ast.Eq()],
                comparators=[ast.Constant(value=idx)],
            )
            # After executing a statement, set __state to the next index.
            assign_state = ast.Assign(
                targets=[ast.Name(id="__state", ctx=ast.Store())],
                value=ast.Constant(value=idx + 1),
            )
            if_body = [stmt, assign_state]
            if_stmt = ast.If(test=condition, body=if_body, orelse=[])
            loop_body.append(if_stmt)

        # Termination: if __state equals the number of original statements, break.
        term_condition = ast.Compare(
            left=ast.Name(id="__state", ctx=ast.Load()),
            ops=[ast.Eq()],
            comparators=[ast.Constant(value=len(node.body))],
        )
        term_if = ast.If(test=term_condition, body=[ast.Break()], orelse=[])
        loop_body.append(term_if)

        # Wrap the if-statements in a while True loop.
        while_loop = ast.While(test=ast.Constant(value=True), body=loop_body, orelse=[])
        new_body.append(while_loop)
        node.body = new_body
        return node

    def visit_FunctionDef(self, node):
        if node.body:
            if self.verbose:
                print(f"Flattening control flow in function: {node.name}")
            node = self.flatten_function(node)
        return node

def flatten(tree, verbose=False):
    flattener = ControlFlowFlattener(verbose)
    return flattener.visit(tree)
