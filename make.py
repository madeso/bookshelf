#!/usr/bin/env python3
# Converts from the source markup format to HTML for the web version.

import glob
import pystache
import os
import re
import subprocess
import typing
import argparse
import time
import datetime
import json

import markdown
# import smartypants

# Assumes cwd is root project dir.

GREEN = '\033[32m'
RED = '\033[31m'
DEFAULT = '\033[0m'
PINK = '\033[91m'
YELLOW = '\033[33m'


def file_exist(file: str) -> bool:
    return os.path.isfile(file)


def run_markdown(contents: str):
    body = markdown.markdown(contents, extensions=['extra', 'def_list', 'codehilite'])
    body = body.replace('<aside markdown="1"', '<aside')
    return body


def change_extension(file: str, extension: str):
    base = os.path.splitext(file)[0]
    return base + "." + extension


class Chapter:
    # if href is None then this is a header
    def __init__(self, title: str, href: str, is_header: bool = False):
        self.title = title
        self.href = href
        self.is_header = is_header
        self.next_chapter = -1
        self.prev_chapter = -1
        self.children = []
    
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
    title = 'My awesome book'
    copyright = '2020 Gustav'
    
    template = 'asset/template'
    index = 'asset/index'
    css = 'html/style.css'
    sass_style = 'asset/style.scss'
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

    def get_chapters(self):
        return [c.title for c in self.chapters]
    
    def get_hrefs(self):
        return [c.href for c in self.chapters if c.is_header]

    def load(self, data):
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
        with open(get_project_file_name(folder), 'r') as f:
            book = Book()
            data = json.loads(f.read())
            book.load(data)
            return book
    else:
        return Book()


def set_book(folder, book: Book):
    with open(get_project_file_name(folder), 'w') as f:
        print(json.dumps(book.save(), indent=4), file=f)


def output_path(extension, pattern):
    return extension + "/" + pattern + "." + extension


def cpp_path(pattern):
    return 'code/cpp/' + pattern + '.h'


def pretty(text):
    '''Use nicer HTML entities and special characters.'''
    text = text.replace(" -- ", "&#8202;&mdash;&#8202;")
    text = text.replace("à", "&agrave;")
    text = text.replace("ï", "&iuml;")
    text = text.replace("ø", "&oslash;")
    text = text.replace("æ", "&aelig;")
    return text


def is_up_to_date(path, output, book: Book, basename, extension: str) -> bool:
    sourcemod = max(os.path.getmtime(path), os.path.getmtime(book.template + extension))

    # todo(Gustav): keep or extend?
    if os.path.exists(cpp_path(basename)):
        sourcemod = max(sourcemod, os.path.getmtime(cpp_path(basename)))

    destmod = 0
    if os.path.exists(output):
        destmod = max(destmod, os.path.getmtime(output))
    
    return sourcemod < destmod


class ParsedMarkdown:
    def __init__(self, title, title_html, section, contents, navigation):
        self.title = title
        self.title_html = title_html
        self.section = section
        self.contents = contents
        self.navigation = navigation


def read_markdown(path: str, extension: str, basename: str) -> ParsedMarkdown:
    """Read the markdown file and preprocess it"""
    title = ''
    title_html = ''
    section = ''
    isoutline = False
    navigation = []
    contents = ''

    with open(path, 'r') as input_file:
        # Read each line, preprocessing the special codes.
        for line in input_file:
            stripped = line.lstrip()
            indentation = line[:len(line) - len(stripped)]

            if stripped.startswith('^'):
                command, _, args = stripped.rstrip('\n').lstrip('^').partition(' ')
                args = args.strip()

                if command == 'title':
                    title = args
                    title_html = title

                    # Remove any discretionary hyphens from the title.
                    title = title.replace('&shy;', '')
                elif command == 'section':
                    section = args
                elif command == 'code':
                    contents = contents + include_code(basename, args, indentation)
                elif command == 'outline':
                    isoutline = True
                else:
                    print("UNKNOWN COMMAND:", command, args)

            elif extension != "xml" and stripped.startswith('#'):
                # Build the page navigation from the headers.
                index = stripped.find(" ")
                headertype = stripped[:index]
                header = pretty(stripped[index:].strip())
                anchor = header.lower().replace(' ', '-')
                anchor = anchor.translate(None, '.?!:/"')

                # Add an anchor to the header.
                contents += indentation + headertype
                contents += '<a href="#' + anchor + '" name="' + anchor + '">' + header + '</a>\n'

                # Build the navigation.
                if len(headertype) == 2:
                    navigation.append((len(headertype), header, anchor))

            else:
                contents += pretty(line)
    
    return ParsedMarkdown(title, title_html, section, contents, navigation)


def generate_chapter_link(book: Book, chapter_index: int, extension: str) -> str:
    if chapter_index < 0:
        return ''
    if chapter_index >= len(book.chapters):
        return ''
        
    return change_extension(book.chapters[chapter_index].href, extension)


def generate_output(parsed_markdown: ParsedMarkdown, template: str, book: Book, chapter: Chapter, extension: str) -> str:
    title_text = parsed_markdown.title
    section_header = ""

    if parsed_markdown.section != "":
        title_text = parsed_markdown.title + " &middot; " + parsed_markdown.section
        section_href = parsed_markdown.section.lower().replace(" ", "-")
        section_header = '<span class="section"><a href="{}.html">{}</a></span>'.format(section_href, parsed_markdown.section)

    prev_link = generate_chapter_link(book, chapter.prev_chapter, extension)
    next_link = generate_chapter_link(book, chapter.next_chapter, extension)

    contents = parsed_markdown.contents

    body = run_markdown(contents)

    # body = smartypants.smartypants(body)

    data = {}
    data['title'] = title_text
    data['section_header'] = section_header
    data['header'] = parsed_markdown.title_html
    data['body'] = body
    data['prev'] = prev_link
    data['next'] = next_link
    data['book_title'] = book.title
    data['copyright'] = book.copyright
    data['navigation'] = navigation_to_html(parsed_markdown.title, parsed_markdown.navigation)

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
    template_file = book.index + '.' + extension
    with open(template_file) as f:
        template = f.read()
    
    name = os.path.splitext(os.path.basename(book.index+'.'+extension))[0]
    output_file = output_path(extension, name)

    data = {}
    data['book_title'] = book.title
    data['copyright'] = book.copyright
    data['toc'] = generate_toc_html(book, extension)
    data['sidebar'] = 'sidebar'
    data['index'] = 'index'
    data['first_page'] = change_extension(book.chapters[0].href, extension)
    data['author'] = 'author'

    with open(output_file, 'w') as out:
        output = pystache_render(template_file, template, data)
        out.write(output)


def format_file(chapter: Chapter, skip_up_to_date: bool, extension: str, stat: Stat, book: Book):
    path = os.path.join('book', chapter.href) # book/the_file.md
    basename = os.path.splitext(chapter.href)[0] # the_file
    output_file = output_path(extension, basename)

    if skip_up_to_date and is_up_to_date(path, output_file, book, basename, extension):
        # See if the HTML is up to date
        return
        
    parsed_markdown = read_markdown(path, extension, basename)

    modified = datetime.datetime.fromtimestamp(os.path.getmtime(path))
    mod_str = modified.strftime('%B %d, %Y')

    with open(book.template + '.' + extension) as f:
        template = f.read()

    # Write the output.
    with open(output_file, 'w') as out:
        output = generate_output(parsed_markdown, template, book, chapter, extension)

        if extension == "xml":
            output = clean_up_xml(output, book)

        out.write(output)

    word_count = len(parsed_markdown.contents.split(None))
    if parsed_markdown.section:
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


def clean_up_xml(output, book: Book) -> str:
    """Takes the XHTML output and massages it to play nicer with InDesign's XML
    import... idiosyncracies."""

    # Split into preformatted code and regular markup sections. We need to treat
    # code blocks specially so we can preserve their formatting.
    in_code = False
    chunks = re.split("(</?pre>)", output)

    def clean_up_code_xml(code):
        # Ditch most code formatting tags.
        code = re.sub(r'<span class="(k|kt|mi|n|nb|nc|nf|nl|o|p)">([^<]+)</span>', r"\2", code)

        # Turn comments into something InDesign can map to a style.
        code = re.sub(r'<span class="(c1|cn)">([^<]+)</span>', r"<comment>\2</comment>", code)

        # Turn newlines into soft returns so code blocks stay one paragraph, except
        # for the last one.
        code = code[:-1].replace("\n", "&#x2028;") + "\n"

        return code

    def fix_link(match):
        tag = match.group(1)
        contents = match.group(2)
        href = re.search(r'href\s*=\s*"([^"]+)"', tag).group(1)

        # If it's not a link to a chapter, just return the contents of the link and
        # strip out the link itself.
        if not href in book.get_hrefs():
            return contents

        # Turn it into a chapter number reference.
        return "{}<chap-ref> ({})</chap-ref>".format(contents, book.get_hrefs().index(href) + 1)

    def clean_up_xhtml(html):
        # Replace chapter links with chapter number references and remove other
        # links.
        html = re.sub(r"<a\s+([^>]+)>([^<]+)</a>", fix_link, html)

        # Ditch newlines in the middle of blocks of text. Out of sheer malice,
        # even though they are meaningless in actual XML, InDesign treats them
        # as significant.
        html = re.sub(r"\n(?<!<)", " ", html)

        # Also collapse redundant whitespace.
        html = re.sub(r" +", " ", html)
        html = html.replace("> <", "><")

        # Re-add newlines after closing paragraph-level tags.
        html = html.replace("</p>", "</p>\n")
        html = html.replace("</h2>", "</h2>\n")
        html = html.replace("</h3>", "</h3>\n")
        html = html.replace("</li>", "</li>\n")
        html = html.replace("</ol>", "</ol>\n")
        html = html.replace("</ul>", "</ul>\n")
        html = html.replace("</pre>", "</pre>\n")
        html = html.replace("</aside>", "</aside>\n")
        html = html.replace("</blockquote>", "</blockquote>\n")

        # TODO: Non-breaking spaces in <code>...</code> sections.
        return html

    result = ""
    for chunk in chunks:
        if chunk == "<pre>":
            in_code = True
            result += chunk
        elif chunk == "</pre>":
            in_code = False
            result += chunk
        else:
            if in_code:
                result += clean_up_code_xml(chunk)
            else:
                result += clean_up_xhtml(chunk)

    return result


def title_to_file(title):
    """Given a title like "Event Queue", converts it to the corresponding file
    name like "event-queue"."""

    return title.lower().replace(" ", "-").replace(",", "")


def navigation_to_html(chapter, headers):
    nav = ''

    # Section headers start two levels deep.
    currentdepth = 1
    for depth, header, anchor in headers:
        if currentdepth == depth:
            nav += '</li><li>\n'

        while currentdepth < depth:
            nav += '<ul><li>\n'
            currentdepth += 1

        while currentdepth > depth:
            nav += '</li></ul>\n'
            currentdepth -= 1

        nav += '<a href="#' + anchor + '">' + header + '</a>'


    # Close the lists.
    while currentdepth > 1:
        nav += '</li></ul>\n'
        currentdepth -= 1

    return nav


def include_code(pattern, index, indentation):
    with open(cpp_path(pattern), 'r') as source:
        lines = source.readlines()

    code = indentation + '        :::cpp\n'
    inblock = False
    omitting = False
    omitting_name = False
    blockindent = 0

    for line in lines:
        stripped = line.strip()

        if inblock:
            if stripped == '//^' + index:
                # End of our block.
                break

            elif stripped == '//^omit':
                omitting = not omitting

            elif stripped == '//^omit ' + index:
                # Omitting a section just for this block. Other blocks that
                # Contain this code may not omit it.
                omitting_name = not omitting_name

            elif stripped.startswith('//^'):
                # A code block comment for another block,
                # so just ignore it. This can occur with
                # nested code blocks.
                pass

            elif not omitting and not omitting_name:
                # Hackish. Can't strip the leading indent off of blank
                # lines.
                if stripped == '':
                    code += '\n'
                else:
                    code_line = line[blockindent:]
                    if len(code_line) > 64:
                        print("Warning long source line ({} chars):\n{}".format(len(code_line), code_line))
                    code += indentation + '        ' + code_line

        else:
            if stripped == '//^' + index:
                inblock = True
                blockindent = len(line) - len(line.lstrip())

    return code


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

    if args.xml:
        extension = "xml"
        # del sys.argv[1]

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


def handle_chapter(args):
    book = get_book(args.folder)
    href = args.href if args.href is not None else title_to_file(args.title)+'.md'
    book.chapters.append(Chapter(args.title, href, is_header=False))
    set_book(args.folder, book)


def handle_header(args):
    book = get_book(args.folder)
    href = args.href if args.href is not None else title_to_file(args.title)+'.md'
    book.chapters.append(Chapter(args.title, href, is_header=True))
    set_book(args.folder, book)



def main():
    parser = argparse.ArgumentParser(description='Create or write a book')
    sub_parsers = parser.add_subparsers(dest='command_name', title='Commands', help='', metavar='<command>')

    sub = sub_parsers.add_parser('watch', help='Watch file for changes')
    sub.add_argument('--folder', help='the folder where to run from', default=os.getcwd())
    sub.set_defaults(func=handle_watch)

    sub = sub_parsers.add_parser('build', help='Build book')
    sub.add_argument('--xml', action='store_true', help='Use XML')
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
