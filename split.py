import argparse
import os
import glob
from typing import List

def split_to_sections(lines: List[str]) -> List[List[str]]:
    sections = []
    section = []
    for line in lines:
        if line.startswith('#'):
            if section:
                sections.append(section)
                section = []
        section.append(line)
    if section:
        sections.append(section)
    return sections

TEXT_DEPTH = 999

def get_sectiion_name(section: List[str]) -> str:
    first = section[0] if section else ''
    arr = first.split(' ', maxsplit=1)
    ret = arr[1] if len(arr) > 1 else ''
    r = ret.rfind('{')
    if r > 0:
        ret = ret[:r]
    return ret

def get_section_depth(section: List[str]) -> int:
    first = section[0] if section else ''
    ret = first.split(' ')[0].count('#')
    return ret if ret > 0 else TEXT_DEPTH

def join_sections(sections: List[List[str]], depth: int) -> List[List[str]]:
    joined = []
    section = []
    for s in sections:
        if get_section_depth(s) == depth:
            if section:
                joined.append(section)
                section = []
        section.extend(s)
    if section:
        joined.append(section)
    return joined


def markdown_split(arg: str, remove_src: bool, dry_run: bool, attach_name: bool):
    FRONTMATTER_SEP = '+++'

    # get directory of the file
    filename = os.path.abspath(arg)
    dir = os.path.dirname(filename)
    print(f"Exporting {filename} to {dir}")

    lines = []
    frontmatter = []

    # extract markdown header
    with open(filename, encoding='utf8') as file:
        first = True
        tomark = True
        for lline in file:
            line = lline.rstrip()
            if first:
                first = False
                frontmatter.append(line)
                continue
            if tomark:
                if line.startswith(FRONTMATTER_SEP):
                    tomark = False
                frontmatter.append(line)
            else:
                lines.append(line)
    
    # split lines into sections
    sections = split_to_sections(lines)

    # remove intro fron the sections
    intro = []
    if len(sections) > 0:
        i = sections[0]
        if get_section_depth(i) == TEXT_DEPTH:
            intro = i
            sections = sections[1:]

    # get lowest headline
    lowest = min(get_section_depth(s) for s in sections)

    joined_sections = join_sections(sections, lowest)
    base = os.path.splitext(os.path.basename(filename))[0]

    path = os.path.join(dir, base, "_index.md")
    write_file(path, frontmatter, intro, dry_run)

    # write all sections to files
    index = 0
    for s in joined_sections:
        index += 1
        name = get_sectiion_name(s).strip()
        folder_name = f"{index:02d}"
        if attach_name:
            folder_name += "-" + name.lower().replace(' ', '-')
        path = os.path.join(dir, base, folder_name, "index.md")
        fm = [
            FRONTMATTER_SEP,
            f"title = \"{name}\"",
            f"weight = {index}0",
            FRONTMATTER_SEP
        ]
        write_file(path, fm, s[1:], dry_run)

    # remove original source file
    if remove_src and not dry_run:
        print(f"Removing {filename}")
        os.remove(filename)


def write_file(path: str, frontmatter: List[str], lines: List[str], dry_run: bool):
    print(f"Writing {path}")
    if dry_run:
        return
    os.makedirs(os.path.dirname(path), exist_ok=True)
    with open(path, 'w', encoding='utf8') as file:
        for line in frontmatter:
            file.write(line + '\n')
        for line in lines:
            file.write(line + '\n')


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("filenames", help="The name of the file or directories to glob to split", nargs='+')
    parser.add_argument("--keep-src", help="Keep the original source file", action="store_true")
    parser.add_argument("--dry-run", help="Do not write any files", action="store_true")
    parser.add_argument("--dont-attach-name", help="Attach the section name to the folder", action="store_true")
    args = parser.parse_args()
    remove_src = not args.keep_src
    dry_run = args.dry_run
    attach_name = not args.dont_attach_name

    # collect all paths first before we start creating and potentially glob more files
    mds = []
    for filename in args.filenames:
        if os.path.isfile(filename):
            mds.append(filename)
        elif os.path.isdir(filename):
            files = glob.glob(filename + '/**/*.md', recursive=True)
            for file in files:
                mds.append(file)
        else:
            print(f"File or directory not found: {filename}")

    for filename in mds:
        markdown_split(filename, remove_src, dry_run, attach_name)

if __name__ == "__main__":
    main()
