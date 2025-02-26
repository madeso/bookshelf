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

def cleanup_name(name: str) -> str:
    replaced = name.replace(' ', '-').lower()

    # remove anything that isn't a-z, 0-9, or a dash
    replaced = ''.join(c for c in replaced if c.isalnum() or c == '-')

    return replaced

def markdown_split(arg: str, remove_src: bool, dry_run: bool, attach_name: bool, use_subfolders: bool):
    FRONTMATTER_SEP = '+++'

    # get directory of the file
    filename = os.path.abspath(arg)
    dir = os.path.dirname(filename)
    base = os.path.splitext(os.path.basename(filename))[0]

    # if we split a "dir" file, don't create a subfolder
    if base == "_index" or base == "index":
        base = ''

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

    # transform [2 3 2 2] for 2 into [(2 3) (2) (2)]
    joined_sections = join_sections(sections, lowest)

    # write all sections to files
    for index0, s in enumerate(joined_sections):
        is_first = index0 == 0
        is_last = index0 == len(joined_sections) - 1
        index = index0 + 1
        name = get_sectiion_name(s).strip()
        folder_name = f"{index:02d}"
        base_folder = folder_name
        if attach_name:
            folder_name += "-" + cleanup_name(name)
        path = os.path.join(dir, base, folder_name, "index.md") if use_subfolders else os.path.join(dir, base, folder_name + ".md")
        fm = [
            FRONTMATTER_SEP,
            f"title = \"{name}\"",
            f"weight = {index}0"
        ]
        if is_first or is_last:
            b2s = lambda b: "true" if b else "false"
            fm.append(f"no_prev = {b2s(is_first)}")
            fm.append(f"no_next = {b2s(is_last)}")
        fm.append(FRONTMATTER_SEP)
        write_file(path, fm, s[1:], dry_run)
        if base_folder != folder_name:
            folder = os.path.join(dir, base, folder_name)
            sources = set(find_base_folder(dir, base, index))
            sources.discard(folder)
            sources = list(sources)
            dst = os.path.join(folder, 'img')
            if len(sources) == 1:
                src = sources[0]
                print(f"Moving {src} to {dst}")
                if not dry_run:
                    os.rename(src, dst)
            else:
                print(f"  no unique folder for {index} in {dir}/{base}: {sources}")

    # write intro page
    path = os.path.join(dir, base, "_index.md")
    write_file(path, frontmatter, intro, dry_run)

    # remove original source file
    if remove_src and filename != path:
        print(f"Removing {filename}")
        if not dry_run:
            os.remove(filename)

def find_base_folder(dir: str, base: str, index: int) -> List[str]:
    sources = []
    folder = os.path.join(dir, base)
    for e in os.listdir(folder):
        d = os.path.join(folder, e)
        if os.path.isdir(d):
            if e.startswith(f"{index}"):
                sources.append(d)
            if e.startswith(f"{index:02d}"):
                sources.append(d)
            if e.startswith(f"{index:03d}"):
                sources.append(d)
    return sources

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
    parser.add_argument("--dont-move", help="Don't move the markdown files to a subfolder", action="store_true")
    args = parser.parse_args()
    remove_src = not args.keep_src
    dry_run = args.dry_run
    attach_name = not args.dont_attach_name
    use_subfolders = not args.dont_move

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
        markdown_split(filename, remove_src, dry_run, attach_name, use_subfolders)

if __name__ == "__main__":
    main()
