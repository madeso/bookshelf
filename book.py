#!/usr/bin/env python3
# Converts from the source markup format to HTML for the web version.

import os
import subprocess
import typing
import argparse
import time
import json

import pystache
import markdown


# todo(Gustav): replace color printing with library
# todo(Gustav): asset/index.<extension> -> templates/<type>/index.<something>
# todo(Gustav): figure out sass/css setup or remove
# todo(Gustav): support epub
# todo(Gustav): make sure watch watches all the files
# todo(Gustav): add sample css and templates
# todo(Gustav): create functions should add a empty markdown


GREEN = '\033[32m'
RED = '\033[31m'
DEFAULT = '\033[0m'
PINK = '\033[91m'
YELLOW = '\033[33m'


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def read_file(path: str) -> str:
    print('reading ' + path)
    with open(path, 'r', encoding='utf-8') as input_file:
        return input_file.read()


def write_file(contents: str, path: str) -> str:
    print('writing ' + path)
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


class Chapter:
    def __init__(self, title: str, href: str, is_header: bool = False):
        self.title = title
        self.href = href
        self.is_header = is_header
        self.next_chapter = -1
        self.prev_chapter = -1
        self.children = []
        self.parent = None

    def generate_html_list(self, extension: str, indent: str):
        html = indent + '<li><a href="{}">{}</a>'.format(change_extension(self.href, extension), self.title)
        if len(self.children) != 0:
            html += '\n' + indent + '    <ul>\n'
            for c in self.children:
                html += c.generate_html_list(extension, indent + '    ') + '\n'
            html += indent + '    </ul>\n' + indent
        html += '</li>'
        return html


class Stat:
    num_chapters = 0
    empty_chapters = 0
    total_words = 0


def get_project_file_name(folder) -> str:
    return os.path.join(folder, '.book.json')


class Book:
    chapter_folder = 'book'
    title = 'My awesome book'
    copyright = '2020 Gustav'
    sidebar_md = 'book/sidebar.md'
    index_md = 'book/index.md'
    author_md = 'book/author.md'
    template = 'templates/template.'
    index = 'templates/index.'
    css = 'html/style.css'
    sass_style = '/style.scss'
    chapters = [
        Chapter("Section", 'section.md', is_header=True),
        Chapter("Chapter", "chapter.md"),
    ]
    root_chapters = []

    def update_chapters(self):
        # start clean
        self.root_chapters = []
        for chapter in self.chapters:
            chapter.children = []

        last_root = None
        for index, chapter in enumerate(self.chapters):
            chapter.prev_chapter = index - 1
            chapter.next_chapter = index + 1
            if chapter.is_header:
                last_root = chapter
                self.root_chapters.append(chapter)
            elif last_root is not None:
                last_root.children.append(chapter)
                chapter.parent = last_root

    def get_chapters(self):
        return [c.title for c in self.chapters]
    
    def get_hrefs(self):
        return [c.href for c in self.chapters if c.is_header]

    def load(self, data):
        self.chapter_folder = data['chapter_folder']
        self.title = data['title']
        self.copyright = data['copyright']
        self.sidebar_md = data['sidebar_md']
        self.index_md = data['index_md']
        self.author_md = data['author_md']
        self.template = data['template']
        self.index = data['index']
        self.css = data['css']
        self.sass_style = data['sass_style']
        chapters = data['chapters']
        self.chapters = []
        for cc in chapters:
            title = cc['title']
            href = cc['href']
            is_header = cc['is_header']
            c = Chapter(title, href, is_header)
            self.chapters.append(c)
        
        self.update_chapters()

    def save(self):
        data = {}

        #  also here
        data['chapter_folder'] = self.chapter_folder
        data['title'] = self.title
        data['copyright'] = self.copyright
        data['sidebar_md'] = self.sidebar_md
        data['index_md'] = self.index_md
        data['author_md'] = self.author_md
        data['template'] = self.template
        data['index'] = self.index
        data['css'] = self.css
        data['sass_style'] = self.sass_style
        chapters = []
        for c in self.chapters:
            cc = {}
            cc['title'] = c.title
            cc['href'] = c.href
            cc['is_header'] = c.is_header
            chapters.append(cc)
        data['chapters'] = chapters
        return data


def get_book(folder) -> Book:
    if file_exist(get_project_file_name(folder)):
        book = Book()
        data = json.loads(read_file(get_project_file_name(folder)))
        book.load(data)
        return book
    else:
        return Book()


def set_book(folder, book: Book):
    write_file(json.dumps(book.save(), indent=4), get_project_file_name(folder))


def output_path(extension, pattern):
    return extension + "/" + pattern + "." + extension


def pretty(text):
    '''Use nicer HTML entities and special characters.'''
    text = text.replace(" -- ", "&#8202;&mdash;&#8202;")
    text = text.replace("à", "&agrave;")
    text = text.replace("ï", "&iuml;")
    text = text.replace("ø", "&oslash;")
    text = text.replace("æ", "&aelig;")
    return text


def is_up_to_date(path, output, book: Book, extension: str) -> bool:
    sourcemod = max(os.path.getmtime(path), os.path.getmtime(book.template + extension))

    destmod = 0
    if os.path.exists(output):
        destmod = max(destmod, os.path.getmtime(output))
    
    return sourcemod < destmod


def generate_chapter_link(book: Book, chapter_index: int, extension: str) -> str:
    if chapter_index < 0:
        return ''
    if chapter_index >= len(book.chapters):
        return ''
        
    return change_extension(book.chapters[chapter_index].href, extension)


def generate_output(contents: str, template: str, book: Book, chapter: Chapter, extension: str) -> str:
    title_text = chapter.title
    section_header = ""

    if chapter.is_header == False:
        parent = chapter.parent
        title_text = chapter.title + " &middot; " + parent.title
        section_href = change_extension(parent.href, extension)
        section_header = '<span class="section"><a href="{}">{}</a></span>'.format(section_href, parent.title)

    prev_link = generate_chapter_link(book, chapter.prev_chapter, extension)
    next_link = generate_chapter_link(book, chapter.next_chapter, extension)

    body = run_markdown(contents)

    # body = smartypants.smartypants(body)

    data = {}
    data['title'] = title_text
    data['section_header'] = section_header
    data['header'] = chapter.title
    data['body'] = body
    data['prev'] = prev_link
    data['next'] = next_link
    data['book_title'] = book.title
    data['copyright'] = book.copyright

    output = pystache_render(chapter.href, template, data)
    
    return output


def generate_toc_html(book: Book, extension: str) -> str:
    html = ''
    for c in book.root_chapters:
        html = html + c.generate_html_list(extension, '  ')
    return html


def pystache_render(filename, template, data):
    renderer = pystache.renderer.Renderer(missing_tags='strict')
    try:
        return renderer.render(template, data)
    except pystache.context.KeyNotFoundError as e:
        print(filename, e)
        return ''


def format_index(book: Book, extension: str):
    template = ''
    template_file = book.index + extension
    template = read_file(template_file)
    
    name = os.path.splitext(os.path.basename(book.index + extension))[0]
    output_file = output_path(extension, name)

    data = {}
    data['book_title'] = book.title
    data['copyright'] = book.copyright
    data['toc'] = generate_toc_html(book, extension)
    data['sidebar'] = run_markdown(read_file(book.sidebar_md))
    data['index'] = run_markdown(read_file(book.index_md))
    data['first_page'] = change_extension(book.chapters[0].href, extension)
    data['author'] = run_markdown(read_file(book.author_md))

    output = pystache_render(template_file, template, data)
    write_file(output, output_file)


def update_wordcount(stat: Stat, contents: str, chapter: Chapter, basename: str):
    word_count = len(contents.split(None))
    if not chapter.is_header:
        stat.num_chapters += 1
        if word_count < 50:
            stat.empty_chapters += 1
            print("    {}".format(basename))
        elif word_count < 2000:
            stat.empty_chapters += 1
            print("{}-{} {} ({} words)".format(YELLOW, DEFAULT, basename, word_count))
        else:
            stat.total_words += word_count
            print("{}✓{} {} ({} words)".format(GREEN, DEFAULT, basename, word_count))
    else:
        # Section header chapters aren't counted like regular chapters.
        print("{}•{} {} ({} words)".format(GREEN, DEFAULT, basename, word_count))


def path_to_chapter(book: Book, chapter: Chapter):
    """ returns book/the_file.md """
    return os.path.join(book.chapter_folder, chapter.href) # book/the_file.md


def format_file(chapter: Chapter, skip_up_to_date: bool, extension: str, stat: Stat, book: Book):
    path = path_to_chapter(book, chapter)
    basename = os.path.splitext(chapter.href)[0] # the_file
    output_file = output_path(extension, basename)

    if skip_up_to_date and is_up_to_date(path, output_file, book, extension):
        # See if the HTML is up to date
        return
        
    contents = read_file(path)
    template = read_file(book.template + extension)

    # Write the output.
    output = generate_output(contents, template, book, chapter, extension)
    write_file(output, output_file)

    update_wordcount(stat, contents, chapter, basename)


def title_to_file(title):
    """Given a title like "Event Queue", converts it to the corresponding file
    name like "event-queue"."""

    return title.lower().replace(" ", "-").replace(",", "")


def format_files(file_filter: typing.Optional[str], skip_up_to_date: bool, book: Book, extension: str, stat: Stat):
    '''Process each markdown file.'''
    format_index(book, extension)
    for chapter in book.chapters:
        if file_filter is None or file_filter in chapter.href:
            format_file(chapter, skip_up_to_date, extension, stat, book)


def check_sass(book: Book):
    sourcemod = os.path.getmtime(book.sass_style)
    destmod = os.path.getmtime(book.css)
    if sourcemod < destmod:
        return

    subprocess.call(['sass', book.sass_style, book.css])
    print("{}✓{} style.css".format(GREEN, DEFAULT))


def handle_watch(args):
    extension = "html"
    book = get_book(args.folder)
    while True:
        stat = Stat()
        format_files(None, True, book, extension, stat)
        check_sass(book)
        time.sleep(0.3)


def handle_build(args):
    extension = "html"
    book = get_book(args.folder)

    file_filter = args.filter
    stat = Stat()

    format_files(file_filter, False, book, extension, stat)

    valid_chapters = stat.num_chapters - stat.empty_chapters
    average_word_count = stat.total_words / valid_chapters if valid_chapters > 0 else 0
    estimated_word_count = stat.total_words + (stat.empty_chapters * average_word_count)
    percent_finished = stat.total_words * 100 / estimated_word_count if estimated_word_count > 0 else 0

    print("{}/~{} words ({}%)".format(stat.total_words, estimated_word_count, percent_finished))


def handle_init(args):
    book = Book()
    set_book(args.folder, book)
    write_file('', book.sidebar_md)
    write_file('', book.index_md)
    write_file('', book.author_md)
    
    # todo(Gustav): write defaults
    # template = 'templates/template.'
    # index = 'templates/index.'
    # css = 'html/style.css'

    for chapter in book.chapters:
        write_file('', path_to_chapter(book, chapter))


def handle_chapter(args):
    book = get_book(args.folder)
    href = args.href if args.href is not None else title_to_file(args.title)+'.md'
    chapter = Chapter(args.title, href, is_header=False)
    book.chapters.append(chapter)
    write_file('', path_to_chapter(book, chapter))
    set_book(args.folder, book)


def handle_header(args):
    book = get_book(args.folder)
    href = args.href if args.href is not None else title_to_file(args.title)+'.md'
    chapter = Chapter(args.title, href, is_header=True)
    book.chapters.append(chapter)
    write_file('', path_to_chapter(book, chapter))
    set_book(args.folder, book)


def main():
    parser = argparse.ArgumentParser(description='Create or write a book')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('watch', help='Watch file for changes')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.set_defaults(func=handle_watch)

    sub = sub_parsers.add_parser('build', help='Build book')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.add_argument('--filter', help='specify a file name filter to just regenerate a subset of the files')
    sub.set_defaults(func=handle_build)

    sub = sub_parsers.add_parser('chapter', help='Add a chapter to the book')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.add_argument('title', help='the title of the chapter')
    sub.add_argument('--href', help='the href of the chapter', default=None)
    sub.set_defaults(func=handle_chapter)

    sub = sub_parsers.add_parser('header', help='Add a header to the book, headers are above chapters')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.add_argument('title', help='the title of the section')
    sub.add_argument('--href', help='the href of the chapter', default=None)
    sub.set_defaults(func=handle_header)

    sub = sub_parsers.add_parser('init', help='Create a new book')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.set_defaults(func=handle_init)

    args = parser.parse_args()
    if args.command_name is not None:
        args.func(args)
    else:
        parser.print_help()

if __name__ == "__main__":
    main()
