#!/usr/bin/env python3
# Converts from the source markup format to HTML for the web version.

# todo(Gustav): copy source images to desination folder
# todo(Gustav): action to transform image to local folder
# todo(Gustav): action to modify markdown and download image
# todo(Gustav): add watcher
# todo(Gustav): support epub

###################################################################################################
# Imports

import os
import typing
import argparse
import time
import json
# import subprocess

# non-standard dependencies
import pystache
import markdown
import colorama


###################################################################################################
# Global setup

from colorama import Fore, Style
colorama.init(strip=True)


###################################################################################################
# Constants

# single file in book root
BOOK_FILE = '.book.json'

# a folder (or file) that is added to a book is considered a chapter
CHAPTER_FILE = '.chapter.json'

# a markdown that is automatically added to the folder first
# index or readme? readme.md goes nice with github browsing but index.html is another standard
CHAPTER_INDEX = 'index.md'


###################################################################################################
# JSON keys

CHAPTER_JSON_CHAPTERS = 'chapters'

BOOK_JSON_CHAPTER = 'chapter'



###################################################################################################
###################################################################################################
###################################################################################################


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def read_file(path: str) -> str:
    # print('reading ' + path)
    with open(path, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def write_file(contents: str, path: str) -> str:
    print('Writing ' + path)
    directory = os.path.dirname(path)
    os.makedirs(directory, exist_ok=True)
    with open(path, 'w', encoding='utf-8') as file_handle:
        print(contents, file=file_handle)


def run_markdown(contents: str):
    body = markdown.markdown(contents, extensions=['extra', 'def_list', 'codehilite'])
    body = body.replace('<aside markdown="1"', '<aside')
    return body


def change_extension(file: str, extension: str):
    base = os.path.splitext(file)[0]
    return base + "." + extension


def pretty(text):
    '''Use nicer HTML entities and special characters.'''
    text = text.replace(" -- ", "&#8202;&mdash;&#8202;")
    text = text.replace("à", "&agrave;")
    text = text.replace("ï", "&iuml;")
    text = text.replace("ø", "&oslash;")
    text = text.replace("æ", "&aelig;")
    return text


def is_all_up_to_date(input_files: typing.List[str], output: str) -> bool:
    sourcemod = 0
    for path in input_files:
        sourcemod = max(sourcemod, os.path.getmtime(path))

    destmod = 0
    if os.path.exists(output):
        destmod = max(destmod, os.path.getmtime(output))

    return sourcemod < destmod


def pystache_render(filename, template, data):
    renderer = pystache.renderer.Renderer(missing_tags='strict')
    try:
        return renderer.render(template, data)
    except pystache.context.KeyNotFoundError as e:
        print(filename, 'ERROR:', e)
        return ''

def parent_folder(folder: str) -> str:
    return os.path.abspath(os.path.join(folder, os.pardir))

def iterate_parent_folders(folder: str) -> typing.Iterable[str]:
    f = folder
    yield folder
    while True:
        child = parent_folder(f)
        if child != f:
            yield child
            f = child
        else:
            break


def book_path_in_folder(folder: str) -> str:
    return os.path.join(folder, BOOK_FILE)


def get_book_file(folder: str) -> typing.Optional[str]:
    book = book_path_in_folder(folder)
    if file_exist(book):
        return book
    return None


def find_book_file(folder: str) -> typing.Optional[str]:
    for f in iterate_parent_folders(folder):
        book = get_book_file(f)
        if book is not None:
            return book
    return None


def get_template_root() -> str:
    return os.path.join(os.path.dirname(__file__), 'templates')


###################################################################################################
###################################################################################################
###################################################################################################


class Templates:
    def __init__(self, folder: str, ext: str):
        self.index = read_file(os.path.join(folder, 'index.' + ext))
        self.template = read_file(os.path.join(folder, 'template.' + ext))


class Stat:
    def __init__(self):
        self.num_chapters = 0
        self.empty_chapters = 0
        self.total_words = 0

    def update(self, contents: str, name: str, is_header: bool):
        word_count = len(contents.split(None))
        if not is_header:
            self.num_chapters += 1
            if word_count < 50:
                self.empty_chapters += 1
                print("    {}".format(name))
            elif word_count < 2000:
                self.empty_chapters += 1
                print("{}-{} {} ({} words)".format(Fore.YELLOW, Style.RESET_ALL, name, word_count))
            else:
                self.total_words += word_count
                print("{}✓{} {} ({} words)".format(Fore.GREEN, Style.RESET_ALL, name, word_count))
        else:
            # Section header chapters aren't counted like regular chapters.
            print("{}•{} {} ({} words)".format(Fore.GREEN, Style.RESET_ALL, name, word_count))

    def print_estimate(self):
        valid_chapters = self.num_chapters - self.empty_chapters
        average_word_count = self.total_words / valid_chapters if valid_chapters > 0 else 0
        estimated_word_count = self.total_words + (self.empty_chapters * average_word_count)
        percent_finished = self.total_words * 100 / estimated_word_count if estimated_word_count > 0 else 0

        print("{}/~{} words ({}%)".format(self.total_words, estimated_word_count, percent_finished))


def generate_chapter_data(filename: str, content: str, template: str) -> str:
    data = {}

    data['body'] = run_markdown(content)

    # todo(Gustav): fix data
    data['title'] = filename
    data['section_header'] = 'section_header'
    data['header'] = filename
    data['prev'] = 'prev'
    data['next'] = 'next'
    data['book_title'] = 'title'
    data['copyright'] = 'copyright'

    return pystache_render(filename, template, data)

def generate_index_data(filename: str, content: str, template: str) -> str:
    data = {}

    data['index'] = run_markdown(content)

    # todo(Gustav): fix data
    data['book_title'] = filename
    data['copyright'] = 'copyright'
    data['toc'] = 'toc'
    data['sidebar'] = 'sidebar'
    data['first_page'] = 'first_page'
    data['author'] = 'author'

    return pystache_render(filename, template, data)


class Chapter:
    def __init__(self):
        self.chapters = []

    def add_chapter(self, chap: str):
        self.chapters.append(chap)

    def from_json(self, data):
        self.chapters = data[CHAPTER_JSON_CHAPTERS]

    def to_json(self):
        data = {}
        data[CHAPTER_JSON_CHAPTERS] = self.chapters
        return data

    def save(self, file_path: str):
        write_file(json.dumps(self.to_json(), indent=4), file_path)

    @staticmethod
    def load(file_path: str) -> 'Chapter':
        book = Chapter()
        data = json.loads(read_file(file_path))
        book.from_json(data)
        return book

    def build(self, source_folder: str, target_folder: str, ext: str, templates: Templates, stat: Stat):
        chapters = []
        if file_exist(os.path.join(source_folder, CHAPTER_INDEX)):
            chapters.append(CHAPTER_INDEX)
        chapters = chapters + [c for c in self.chapters]

        for chapter in chapters:
            source = os.path.join(source_folder, chapter)
            target = os.path.join(target_folder, change_extension(chapter, ext))
            content = read_file(source)
            stat.update(content, chapter, len(self.chapters) > 0)
            is_index = chapter == CHAPTER_INDEX
            generated = generate_index_data(chapter, content, templates.index) if is_index else generate_chapter_data(chapter, content, templates.template)
            write_file(generated, target)


class Book(Chapter):
    def from_json(self, data):
        super().from_json(data[BOOK_JSON_CHAPTER])

    def to_json(self):
        data = {}
        data[BOOK_JSON_CHAPTER] = super().to_json()
        return data

    def save(self, file_path: str):
        write_file(json.dumps(self.to_json(), indent=4), file_path)

    @staticmethod
    def load(file_path: str) -> 'Book':
        book = Book()
        data = json.loads(read_file(file_path))
        book.from_json(data)
        return book




###################################################################################################
###################################################################################################
###################################################################################################


def handle_watch(_):
    while True:
        # check files
        time.sleep(0.3)


def handle_init(_):
    root = os.getcwd()
    path = find_book_file(root)
    if path is not None:
        print('Book is already defined in {}'.format(path))
    else:
        path = book_path_in_folder(root)
        book = Book()
        book.save(path)
        print('Created book!')


def handle_add(args):
    root = os.getcwd()
    path = get_book_file(root)
    if path is None:
        print('This is not a book!')
        return

    book = Book.load(path)

    changed = False
    for chapter in args.chapters:
        chapter_path = os.path.join(root, chapter)
        if not file_exist(chapter_path):
            print("File '{}' doesn't exist".format(chapter_path))
            continue
        book.add_chapter(chapter)
        print("Adding {}".format(chapter))
        changed = True

    if changed:
        book.save(path)


def handle_build(_):
    root = os.getcwd()
    ext = 'html'

    path = find_book_file(root)
    if path is None:
        print('This is not a book')
        return

    book = Book.load(path)
    book_folder = os.path.dirname(path)
    html = os.path.join(book_folder, 'html')
    stat = Stat()
    templates = Templates(get_template_root(), ext)

    book.build(book_folder, html, ext, templates, stat)

    # generate
    stat.print_estimate()



###################################################################################################
###################################################################################################
###################################################################################################


def main():
    parser = argparse.ArgumentParser(description='Create or write a book')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('init', help='Create a new book')
    sub.set_defaults(func=handle_init)

    sub = sub_parsers.add_parser('add', help='Add a thing to a book')
    sub.add_argument('chapters', nargs='+', metavar='chapter')
    sub.set_defaults(func=handle_add)

    sub = sub_parsers.add_parser('build', help='Generate html')
    sub.set_defaults(func=handle_build)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()


###################################################################################################
###################################################################################################
###################################################################################################


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        pass
