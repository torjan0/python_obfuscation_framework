import ast
import random
import string

def generate_random_name(length=8):
    return "v_" + "".join(random.choices(string.ascii_letters + string.digits, k=length))

class VariableMangler(ast.NodeTransformer):
    def __init__(self, verbose=False):
        self.verbose = verbose
        self.name_map = {}
        self.imported_names = set()

    def visit_Import(self, node):
        # Record top-level module names or alias names.
        for alias in node.names:
            if alias.asname:
                self.imported_names.add(alias.asname)
            else:
                self.imported_names.add(alias.name.split('.')[0])
        return node

    def visit_ImportFrom(self, node):
        # Record names imported via "from ... import ..."
        for alias in node.names:
            if alias.asname:
                self.imported_names.add(alias.asname)
            else:
                self.imported_names.add(alias.name)
        return node

    def visit_Name(self, node):
        # Don't rename built-ins or imported names.
        if node.id in {"print", "len", "range", "int", "str", "float", "True", "False", "None", "decrypt_string"}:
            return node
        if node.id in self.imported_names:
            return node
        if node.id not in self.name_map:
            new_name = generate_random_name()
            self.name_map[node.id] = new_name
            if self.verbose:
                print(f"Renaming variable {node.id} to {new_name}")
        node.id = self.name_map[node.id]
        return node

def mangle(tree, verbose=False):
    mangler = VariableMangler(verbose)
    return mangler.visit(tree)
