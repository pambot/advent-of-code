import sys
import os

if __name__ == "__main__":
    year, day = map(int, sys.argv[1:3])
    os.system(f"python solutions/{year}/{day:02d}.py")
