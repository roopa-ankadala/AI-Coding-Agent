import os
import shutil
import subprocess


BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_FOLDER = os.path.join(BASE_DIR, "project_files")
BACKUP_FOLDER = os.path.join(BASE_DIR, "backups")

def backup_file(file_path):
    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    filename = os.path.basename(file_path)

    shutil.copy(
        file_path,
        os.path.join(BACKUP_FOLDER, filename)
    )


def summarize_file(filepath):
    with open(filepath, "r") as f:
        lines = f.readlines()

    functions = []

    for line in lines:
        if line.strip().startswith("def "):
            functions.append(
                line.strip()
            )

    return {
    "file": os.path.basename(filepath),
    "functions": functions
}


def build_project_context():
    context = []

    for file in os.listdir(PROJECT_FOLDER):
        if file.endswith(".py"):

            filepath = os.path.join(
                PROJECT_FOLDER,
                file
            )

            context.append(
                summarize_file(filepath)
            )

    return context


def apply_changes():

    calculator_path = os.path.join(
        PROJECT_FOLDER,
        "calculator.py"
    )

    backup_file(calculator_path)

    with open(calculator_path, "w") as f:
        f.write(
'''def add(a, b):
    return a + b

def subtract(a, b):
    return a - b

def divide(a, b):
    if b == 0:
        raise ValueError("Cannot divide by zero")
    return a / b
'''
        )

    test_path = os.path.join(
        PROJECT_FOLDER,
        "test_calculator.py"
    )

    backup_file(test_path)

    with open(test_path, "w") as f:
        f.write(
'''from calculator import add, divide

assert add(2,3) == 5

assert divide(10,2) == 5

try:
    divide(10,0)
    assert False
except ValueError:
    pass

print("All tests passed!")
'''
        )


def run_tests():

    result = subprocess.run(
        ["python", "test_calculator.py"],
        cwd=PROJECT_FOLDER,
        capture_output=True,
        text=True
    )

    print(result.stdout)

    if result.stderr:
        print(result.stderr)


print("PROJECT SUMMARY")
print(build_project_context())

print()

apply_changes()

print("FILES UPDATED")

run_tests()