import ast

class MetadataStripper(ast.NodeTransformer):
    def visit_FunctionDef(self, node):
        # Remove a function's docstring if present.
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
            node.body.pop(0)
        return self.generic_visit(node)

    def visit_Module(self, node):
        # Remove a module-level docstring if present.
        if (node.body and isinstance(node.body[0], ast.Expr) and 
            isinstance(node.body[0].value, ast.Constant) and isinstance(node.body[0].value.value, str)):
            node.body.pop(0)
        return self.generic_visit(node)

def strip_metadata(tree):
    stripper = MetadataStripper()
    return stripper.visit(tree)
