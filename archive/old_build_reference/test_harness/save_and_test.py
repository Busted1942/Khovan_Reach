#!/usr/bin/env python3
"""Autosave current work as a WIP commit, run tests, and revert the WIP commit on failure.

Usage: python save_and_test.py

Behavior:
- If working tree is clean, runs tests and exits with pytest return code.
- If there are changes, stages all, creates a `WIP auto-save` commit, runs tests.
  - On success: leaves the WIP commit so you have a saved checkpoint to amend or squash later.
  - On failure: undoes the WIP commit (keeps your working tree intact) and exits non-zero.
"""
import os
import subprocess
import sys
from datetime import datetime

def run(cmd, check=False):
    return subprocess.run(cmd, shell=True, check=check)

def git_has_changes():
    res = subprocess.run(['git','status','--porcelain'], capture_output=True, text=True)
    return bool(res.stdout.strip())

def main():
    # If no changes, just run tests
    if not git_has_changes():
        return subprocess.call([sys.executable, 'run_tests.py'])

    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    msg = f'WIP auto-save {timestamp}'

    # Stage all changes and create WIP commit
    rc = subprocess.call(['git','add','-A'])
    if rc != 0:
        print('git add failed', file=sys.stderr)
        return rc

    rc = subprocess.call(['git','commit','-m', msg, '--no-verify'])
    if rc != 0:
        print('git commit failed', file=sys.stderr)
        return rc

    # Run tests
    rc = subprocess.call([sys.executable, 'run_tests.py'])
    if rc == 0:
        print('Tests passed — WIP commit created. You can amend or squash later.')
        return 0

    # Tests failed — undo the WIP commit but keep working tree
    print('Tests failed — reverting WIP commit, keeping worktree.', file=sys.stderr)
    subprocess.call(['git','reset','--mixed','HEAD~1'])
    return rc

if __name__ == '__main__':
    sys.exit(main())
