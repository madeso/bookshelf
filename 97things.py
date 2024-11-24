import argparse
import os
import glob
from typing import List


def fix(dir: str):
    print(dir)

    entries = (os.path.join(dir, p) for p in os.listdir(dir))
    dirs = list(p for p in entries if os.path.isdir(p))

    print(f"{dir} has {len(dirs)} directories")
    for d in dirs:
        src = os.path.join(d, 'readme.md')
        lines = []
        with open(src, 'r') as f:
            lines = f.readlines()
        if len(lines) == 0:
            print(f"Empty file: {src}")
            continue
        if not lines[0].startswith('# '):
            print(f"Not a valid file: {src}")
            continue
        title = lines[0][2:].strip()
        name = os.path.split(d)[1]
        weight = name.split('_')[1].lstrip('0')
        tgt = os.path.join(dir, f"{name}.md")
        escaped_title = title.replace('"', '\\"')
        with open(tgt, 'w') as f:
            f.write('+++\n')
            f.write(f"title = \"{weight}: {escaped_title}\"\n")
            f.write(f"weight = {weight}\n")
            f.write('+++\n')
            f.write(''.join(lines[1:]))


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", help="The name of the file or directories to glob to split", nargs='+')
    args = parser.parse_args()

    for filename in args.filenames:
        fix(os.path.abspath(filename))

if __name__ == "__main__":
    main()
