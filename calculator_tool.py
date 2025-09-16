import ast
import operator as op

# Supported operators
operators = {
    ast.Add: op.add,
    ast.Sub: op.sub,
    ast.Mult: op.mul,
    ast.Div: op.truediv,
    ast.Pow: op.pow,
    ast.BitXor: op.xor,
    ast.USub: op.neg
}

def eval_expr(expr):
    """
    Safely evaluates a string expression.
    """
    return eval_(ast.parse(expr, mode='eval').body)

def eval_(node):
    """
    Recursively evaluates an AST node.
    """
    if isinstance(node, ast.Num):  # <number>
        return node.n
    elif isinstance(node, ast.BinOp):  # <left> <operator> <right>
        return operators[type(node.op)](eval_(node.left), eval_(node.right))
    elif isinstance(node, ast.UnaryOp):  # <operator> <operand> e.g., -1
        return operators[type(node.op)](eval_(node.operand))
    else:
        raise TypeError(node)

def calculate(expression: str) -> str:
    """
    Safely evaluates a mathematical expression using an AST parser
    and returns the result. Supports addition, subtraction,
    multiplication, and division, and respects order of operations.

    Args:
        expression: The mathematical expression to evaluate.

    Returns:
        The result of the calculation as a string, or an error message.
    """
    try:
        result = eval_expr(expression)
        return str(result)
    except (TypeError, SyntaxError, KeyError, ZeroDivisionError) as e:
        return f"Error: Invalid or unsupported expression. Reason: {e}"
    except Exception as e:
        return f"An unexpected error occurred: {e}"
