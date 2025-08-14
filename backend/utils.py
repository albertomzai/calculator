import ast

ALLOWED_OPERATORS = {
    ast.Add,
    ast.Sub,
    ast.Mult,
    ast.Div,
    ast.Pow,
}

def _eval(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    elif hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Only numeric constants are allowed')
    elif isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _eval(node.left)
        right = _eval(node.right)
        if isinstance(node.op, ast.Add):
            return left + right
        if isinstance(node.op, ast.Sub):
            return left - right
        if isinstance(node.op, ast.Mult):
            return left * right
        if isinstance(node.op, ast.Div):
            return left / right
        if isinstance(node.op, ast.Pow):
            return left ** right
    else:
        raise ValueError('Unsupported expression')

def safe_eval(expr: str):
    """Evaluate a mathematical expression safely.

    Only supports +, -, *, /, and ** with numeric literals.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Invalid syntax') from e

    if not isinstance(parsed.body, (ast.BinOp, ast.UnaryOp, ast.Num) if hasattr(ast, 'Num') else (ast.BinOp, ast.UnaryOp, ast.Constant)):
        # Allow only binary operations and constants
        raise ValueError('Expression must be a simple arithmetic expression')

    return _eval(parsed.body)