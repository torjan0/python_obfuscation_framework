import os
import ast
import traceback

from obfuscator import (
    variable_mangler, 
    string_encryptor, 
    control_flow_flattener, 
    dead_code_injector,
    opaque_predicates,
    metadata_stripper
)

def process_directory(directory, level, verbose=False):
    """Walk through the directory and process all .py files."""
    if os.path.isdir(directory):
        for root, _, files in os.walk(directory):
            for file in files:
                if file.endswith(".py"):
                    file_path = os.path.join(root, file)
                    if verbose:
                        print(f"Processing file: {file_path}")
                    process_file(file_path, level, verbose)
    else:
        # Single file mode.
        process_file(directory, level, verbose)

def process_file(file_path, level, verbose=False):
    """Parse, transform, and write back a Python file."""
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            source_code = f.read()
        tree = ast.parse(source_code, filename=file_path)

        # Apply transformations based on obfuscation level.
        if level in ["light", "medium", "heavy"]:
            tree = variable_mangler.mangle(tree, verbose)

        if level in ["medium", "heavy"]:
            tree = string_encryptor.encrypt_strings(tree, verbose)

        if level == "heavy":
            tree = control_flow_flattener.flatten(tree, verbose)
            tree = dead_code_injector.inject_dead_code(tree, verbose)
            tree = opaque_predicates.inject_opaque_predicates(tree, verbose)
            tree = metadata_stripper.strip_metadata(tree)

        # Fix missing location information.
        tree = ast.fix_missing_locations(tree)

        # Unparse AST back into source code.
        new_code = ast.unparse(tree)
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_code)
        if verbose:
            print(f"Obfuscation complete for {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
        traceback.print_exc()