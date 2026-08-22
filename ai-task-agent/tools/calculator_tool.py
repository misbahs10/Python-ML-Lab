def calculate(expression: str) -> str:
    """Math expression evaluate karta hai, jaise '25*17'"""
    try:
        result = eval(expression, {"__builtins__": {}})
        return str(result)
    except Exception as e:
        return f"Error: {e}"