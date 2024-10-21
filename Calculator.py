# src/ASLUMpy/Calculator.py
# calculator.py
from Calculator import add, subract, multiply, divide  # Import Keff from functions.py



def add(x, y):
    """Add Function"""
    return x + y

def subtract(x, y):
    """Subtract Function"""
    return x - y

def multiply(x, y):
    """Multiply Function"""
    return x * y

def divide(x, y):
    """Divide Function"""
    if y == 0:
        raise ValueError("Can not divide by zero!")
    return x / y


