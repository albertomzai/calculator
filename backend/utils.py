import ast

__ALLOWED_OPERATORS = {ast.Add, ast.Sub, ast.Mult, ast.Div}

def _eval_node(node):
    if isinstance(node, ast.Num):  # Python <3.8
        return node.n
    if isinstance(node, ast.Constant):  # Python >=3.8
        if isinstance(node.value, (int, float)):
            return node.value
        raise ValueError('Unsupported constant type')

    if isinstance(node, ast.BinOp) and type(node.op) in __ALLOWED_OPERATORS:
        left = _eval_node(node.left)
        right = _eval_node(node.right)
        if isinstance(node.op, ast.Add): return left + right
        if isinstance(node.op, ast.Sub): return left - right
        if isinstance(node.op, ast.Mult): return left * right
        if isinstance(node.op, ast.Div): return left / right

    raise ValueError('Unsupported expression')

def safe_eval(expr: str):
    """Evaluate a mathematical expression containing only +,-,*,/ operators."""
    try:
        parsed = ast.parse(expr, mode='eval')
    except SyntaxError as e:
        raise ValueError('Syntax error in expression') from e

    if not isinstance(parsed.body, (ast.BinOp, ast.UnaryOp, ast.Num, ast.Constant)) and not isinstance(parsed.body, ast.Expression):
        # Allow only simple expressions
        pass

    return _eval_node(parsed.body)