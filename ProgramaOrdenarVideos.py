import subprocess
import sys

venv_python = sys.executable  # Obtiene la ruta al Python actual

test_files = [
    "AgregarALista.py",
    "OrdenarLista.py"
    ]

for test_file in test_files:
    try:
        result = subprocess.run([venv_python, test_file], check=True)
        print(f"Test {test_file} completed successfully.")
    except subprocess.CalledProcessError as e:
        print(f"An error occurred while running {test_file}: {e}")
    except FileNotFoundError as e:
        print(f"File {test_file} not found: {e}")