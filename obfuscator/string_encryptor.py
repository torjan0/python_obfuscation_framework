import ast
import base64
import os
from Crypto.Cipher import AES

def pad(s):
    # PKCS#7 padding
    padding_len = 16 - (len(s) % 16)
    return s + (chr(padding_len) * padding_len)

def encrypt_string(plain_text, key):
    plain_text_padded = pad(plain_text)
    cipher = AES.new(key, AES.MODE_CFB)
    ct_bytes = cipher.encrypt(plain_text_padded.encode("utf-8"))
    # Prepend the IV to the ciphertext.
    encrypted = cipher.iv + ct_bytes
    return base64.b64encode(encrypted).decode("utf-8")

def ensure_decrypt_function(tree):
    """
    If the module does not already define decrypt_string, insert it.
    """
    func_name = "decrypt_string"
    for node in tree.body:
        if isinstance(node, ast.FunctionDef) and node.name == func_name:
            return tree  # already exists

    func_code = '''
def decrypt_string(enc_str, key_str):
    import base64
    from Crypto.Cipher import AES
    enc = base64.b64decode(enc_str)
    key = base64.b64decode(key_str)
    iv = enc[:AES.block_size]
    ct = enc[AES.block_size:]
    cipher = AES.new(key, AES.MODE_CFB, iv)
    pt = cipher.decrypt(ct).decode('utf-8')
    padding_len = ord(pt[-1])
    return pt[:-padding_len]
'''
    func_node = ast.parse(func_code).body[0]
    tree.body.insert(0, func_node)
    return tree

class StringEncryptor(ast.NodeTransformer):
    def __init__(self, key, verbose=False):
        self.key = key
        self.verbose = verbose

    def visit_Constant(self, node):
        # Process only non-empty string constants.
        # This handles strings that are not part of f-strings.
        if isinstance(node.value, str) and node.value:
            plain_text = node.value
            encrypted = encrypt_string(plain_text, self.key)
            key_b64 = base64.b64encode(self.key).decode("utf-8")
            if self.verbose:
                print(f"Encrypting string: {plain_text} -> {encrypted}")
            # Replace the literal with a call: decrypt_string("encrypted", "key")
            new_node = ast.Call(
                func=ast.Name(id="decrypt_string", ctx=ast.Load()),
                args=[ast.Constant(value=encrypted), ast.Constant(value=key_b64)],
                keywords=[],
            )
            return ast.copy_location(new_node, node)
        return node

    def visit_JoinedStr(self, node):
        # Process each value in the f-string.
        new_values = []
        for value in node.values:
            # If it's a Constant string, process it.
            if isinstance(value, ast.Constant) and isinstance(value.value, str) and value.value:
                plain_text = value.value
                encrypted = encrypt_string(plain_text, self.key)
                key_b64 = base64.b64encode(self.key).decode("utf-8")
                if self.verbose:
                    print(f"Encrypting string in f-string: {plain_text} -> {encrypted}")
                call_node = ast.Call(
                    func=ast.Name(id="decrypt_string", ctx=ast.Load()),
                    args=[ast.Constant(value=encrypted), ast.Constant(value=key_b64)],
                    keywords=[],
                )
                # Wrap the call in a FormattedValue so it's valid inside a JoinedStr.
                formatted_value = ast.FormattedValue(
                    value=call_node,
                    conversion=-1,
                    format_spec=None
                )
                new_values.append(formatted_value)
            else:
                # For other nodes, visit recursively.
                new_values.append(self.visit(value))
        node.values = new_values
        return node

def encrypt_strings(tree, verbose=False):
    # Generate a random AES key (16 bytes)
    key = os.urandom(16)
    encryptor = StringEncryptor(key, verbose)
    tree = encryptor.visit(tree)
    tree = ensure_decrypt_function(tree)
    return tree
