Portfolio Coding Agent CLI

Features: 
Read project files
Build project context
Plan file modifications
Apply coordinated edits
Create backups
Run tests automatically
Dry-run mode
Attempt logging

Architecture:

    User Task 
        ↓ 
    Read Project 
        ↓ 
    Build Context 
        ↓ 
    Plan Changes 
        ↓ 
    Apply Fixes 
        ↓ 
    Run Tests
        ↓ 
    Observe Results 
        ↓ 
    Retry if Needed

Usage:
python agent.py --project project_files --task "fix divide by zero bug"

Dry Run:
python agent.py --project project_files --task "fix divide by zero bug" --dry-run