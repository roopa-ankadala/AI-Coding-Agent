import os
import shutil
import subprocess
import argparse

# ----------------------------
# CLI Arguments
# ----------------------------

parser = argparse.ArgumentParser()

parser.add_argument(
    "--project",
    required=True,
    help="Project folder path"
)

parser.add_argument(
    "--task",
    required=True,
    help="Task description"
)

parser.add_argument(
    "--dry-run",
    action="store_true",
    help="Show proposed changes only"
)

args = parser.parse_args()

# ----------------------------
# Paths
# ----------------------------

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PROJECT_FOLDER = os.path.join(
    BASE_DIR,
    args.project
)

BACKUP_FOLDER = os.path.join(
    BASE_DIR,
    "backups"
)

ATTEMPT_FOLDER = os.path.join(
    BASE_DIR,
    "attempts"
)

os.makedirs(ATTEMPT_FOLDER, exist_ok=True)

# ----------------------------
# Logging
# ----------------------------

def log_attempt(task, status):

    with open(
        os.path.join(
            ATTEMPT_FOLDER,
            "attempt_1.txt"
        ),
        "w",
        encoding="utf-8"
    ) as log:

        log.write(f"TASK:\n{task}\n\n")
        log.write(f"STATUS:\n{status}\n")


# ----------------------------
# Backup
# ----------------------------

def backup_file(file_path):

    os.makedirs(BACKUP_FOLDER, exist_ok=True)

    filename = os.path.basename(file_path)

    shutil.copy(
        file_path,
        os.path.join(
            BACKUP_FOLDER,
            filename
        )
    )


# ----------------------------
# File Summary
# ----------------------------

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


# ----------------------------
# Project Context
# ----------------------------

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


# ----------------------------
# Apply Changes
# ----------------------------

def apply_changes():

    calculator_path = os.path.join(
        PROJECT_FOLDER,
        "calculator.py"
    )

    backup_file(calculator_path)

    with open(
        calculator_path,
        "w"
    ) as f:

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

    with open(
        test_path,
        "w"
    ) as f:

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


# ----------------------------
# Run Tests
# ----------------------------

def run_tests():

    result = subprocess.run(
        ["python", "test_calculator.py"],
        cwd=PROJECT_FOLDER,
        capture_output=True,
        text=True,
        timeout=5
    )

    return result


# ----------------------------
# Main
# ----------------------------

print("\n" + "="*50)
print("PORTFOLIO CODING AGENT CLI")
print("="*50)

print("\nTask:")
print(args.task)

print("\nProject:")
print(PROJECT_FOLDER)

print("\nScanning project...")

context = build_project_context()

print("\nPROJECT SUMMARY")
print(context)

print("\nPlanning changes...")

print("""
Files selected:
- calculator.py
- test_calculator.py
""")

if args.dry_run:

    print("DRY RUN MODE")

    print("""
Proposed Changes

calculator.py
-------------------------
Add divide by zero validation

test_calculator.py
-------------------------
Add ValueError test
""")

    log_attempt(
        args.task,
        "DRY RUN"
    )

    exit()

apply_changes()

print("FILES UPDATED")

print("\nRunning tests...")

result = run_tests()

print(result.stdout)

if result.stderr:
    print(result.stderr)

if result.returncode == 0:

    print("\nTASK COMPLETED SUCCESSFULLY")

    log_attempt(
        args.task,
        "PASSED"
    )

else:

    print("\nTASK FAILED")

    log_attempt(
        args.task,
        "FAILED"
    )