# src/ASLUMpy/Calculator.py

from .functions import Keff  # Import Keff from functions.py

def main():
    result = Keff(0.5)
    print(f"Keff result: {result}")

if __name__ == "__main__":
    main()

