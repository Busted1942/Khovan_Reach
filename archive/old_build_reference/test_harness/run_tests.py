#!/usr/bin/env python3
import sys
import subprocess

def main():
    ret = subprocess.call([sys.executable, "-m", "pytest", "-q", "--maxfail=1"])
    raise SystemExit(ret)

if __name__ == '__main__':
    main()
