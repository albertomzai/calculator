import ast

ALLOWED_OPERATORS = {
    ast.Add, ast.Sub, ast.Mult, ast.Div, ast.Pow,
    ast.UAdd, ast.USub
}

def _eval_node(node):
    """Recursively evaluate an AST node if it is allowed."""
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if hasattr(ast, 'Constant') and isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError(f'Unsupported constant type: {type(node.value).__name__}')

    if isinstance(node, ast.BinOp) and type(node.op) in ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        op_type = type(node.op)
        if op_type is ast.Add:
            return left + right
        if op_type is ast.Sub:
            return left - right
        if op_type is ast.Mult:
            return left * right
        if op_type is ast.Div:
            return left / right
        if op_type is ast.Pow:
            return left ** right

    if isinstance(node, ast.UnaryOp) and type(node.op) in ALLOWED_OPERATORS:
        operand = _eval_node(node.operand)
        if isinstance(node.op, ast.UAdd):
            return +operand
        if isinstance(node.op, ast.USub):
            return -operand

    raise ValueError(f'Unsupported expression: {ast.dump(node)}')

def safe_eval(expr: str):
    """Safely evaluate a mathematical expression string.

    Only basic arithmetic operators are allowed. Raises ValueError on
    disallowed nodes or syntax errors.
    """
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError(f'Syntax error in expression: {e}') from None

    # The body of an eval node is a single expression
    if not isinstance(parsed.body, (ast.Expression, ast.BinOp, ast.UnaryOp, ast.Num, getattr(ast, 'Constant', None))):
        raise ValueError('Expression must be a single arithmetic expression')

    return _eval_node(parsed.body)