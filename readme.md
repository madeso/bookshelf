# book.py
The elevator pitch of this script is to take markdown and generate a beautiful book with no extra work.

## Usage

Download or clone to some folder and (optionally add it as a alias in your shell startup):

```sh
alias book path/to/book.py
```

Then start creating it

```sh
# create a folder for our book
mkdir my-book
cd my-book
git init

# init the book
book init

# update front page and book title
vi index.md

# write the first chapter
vi chapter.md

# and add it to the book
book add chapter.md

# generate the book
book build

# and enjoy the fruits of your labor
open html/index.html
```

Enjoy!


## Samples/Credits

HTHL template is based on/inspired by the online version of [programming patterns book](http://gameprogrammingpatterns.com/)

The test book is a [loren ipsum](https://www.lipsum.com/) generated book.

The ui book is a 'book' copied from on a [blog series by Joel Spolsky](https://www.joelonsoftware.com/2001/10/24/user-interface-design-for-programmers/)

The cli book is from [clig.dev](https://clig.dev/) and it's [markdown source](https://github.com/cli-guidelines/cli-guidelines).
