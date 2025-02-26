+++
title = "Comments"
weight = 30
+++

### John

Let's move on to the second area of disagreement: comments. In my opinion,
the _Clean Code_ approach to commenting results in code with
inadequate documentation, which increases the cost of software development.
I'm sure you disagree, so let's discuss.

Here is what _Clean Code_ says about comments (page 54):

> The proper use of comments is to compensate for our failure to express
> ourselves in code. Note that I use the word failure. I meant it.
> Comments are always failures. We must have them because we cannot always
> figure out how to express ourselves without them, but their use is not
> a cause for celebration... Every time you write a comment, you should
> grimace and feel the failure of your ability of expression.

I have to be honest: I was horrified when I first read this text, and it
still makes me cringe. This stigmatizes writing comments. Junior developers
will think "if I write comments, people may think I've failed, so the
safest thing is to write no comments."

### UB

That chapter begins with these words:

> _Nothing can be quite so helpful as a well placed comment._

It goes on to say that comments are a _necessary_ evil.

The only way a reader could infer that they should write no comments is if they hadn't actually read the chapter. The chapter walks through a series of comments, some bad, some good.

### John

_Clean Code_ focuses a lot more on the "evil" aspects of comments than the
"necessary" aspects. The sentence you quoted above is followed by two
sentences criticizing comments. Chapter 4 spends 4 pages talking about good
comments, followed by 15 pages talking about bad comments. There are snubs
like "the only truly good comment is the comment you found a way
not to write". And "Comments are always failures" is so catchy
that it's the one thing readers are most likely to remember from the
chapter.

### UB

The difference in page count is because there are just a few ways to write good comments, and so many more ways to write bad ones.

### John

I disagree; this illustrates your bias against comments. If you look at
Chapter 13 of APOSD, it finds a lot more
constructive ways to use comments than _Clean Code_. And if you compare
the tone of Chapter 13 of APOSD with Chapter 4 of _Clean Code_, the hostility
of _Clean Code_ towards comments becomes pretty clear.

### UB

I'll leave you to balance that last comment with the initial statement, and the final example, in the _Comments_ chapter. They do not communicate "hostility".

I'm not hostile to comments in general. I _am_ very hostile to gratuitous comments.

You and I likely both survived through a time when comments were absolutely necessary. In the '70s and '80s I was an assembly language programmer. I also wrote a bit of FORTRAN. Programs in those languages that had no comments were impenetrable.

As a result it became conventional wisdom to write comments by default. And, indeed, computer science students were taught to write comments uncritically. Comments became _pure good_.

In _Clean Code_ I decided to fight that mindset. Comments can be _really bad_ as well as good.

### John

I don't agree that comments are less necessary today than they were
40 years ago.

Comments are crucially important and add enormous value to software.
The problem is that there is a lot of important information that simply
cannot be expressed in code. By adding comments to fill in this missing
information, developers can make code dramatically easier to read.
This is not a "failure of their ability to express themselves", as you
put it.

### UB

It's very true that there is important information that is not, or cannot be, expresssed in code. That's a failure. A failure of our languages, or of our ability to use them to express ourselves. In every case a comment is a failure of our ability to use our languages to express our intent.

And we fail at that very frequently, and so comments are a necessary evil -- or, if you prefer, _an unfortunate necessity_. If we had the perfect programming language (TM) we would never write another comment.

### John

I don't agree that a perfect programming language would
eliminate the need for comments. Comments and code serve very different
purposes, so it's not obvious to me that we should use the same
language for both. In my experience, English works quite well
as a language for comments.
Why do you feel that information about a program should
be expressed entirely in code, rather than using a combination of code
and English?

### UB

I bemoan the fact that we must sometimes use a human language instead of a programming language. Human languages are imprecise and full of ambiguities. Using a human language to describe something as precise as a program is very hard, and fraught with many opportunities for error and inadvertent misinformation.

### John

I agree that English isn't always as precise as code, but it can still be
used in precise ways and comments typically don't need the same
degree of precision as code.
Comments often contain qualitative information such
as _why_ something is being done, or the overall idea of something.
English works better for these than code because it is a more
expressive language.

### UB

I have no argument with that statement.

### John

Are you concerned that comments will be incorrect or
misleading and that this will slow down software development?
I often hear people complain about stale comments (usually as an excuse
for writing no comments at all) but
I have not found them be a significant problem
over my career. Incorrect comments do happen, but I don't encounter them
very often and when I do, they rarely cost me much time. In contrast, I waste
_enormous_ amounts of time because of inadequate documentation; it's not
unusual for me to spend 50-80% of my development time wading through
code to figure out things that would be obvious if the code was properly
commented.

### UB

You and I have had some very different experiences.

I have certainly been helped by well placed comments. I have also, just as certainly, (and within this very document) been distracted and confused by a comment that was incorrect, misplaced, gratuitous, or otherwise just plain bad.

### John

I invite everyone reading this article to ask yourself the following questions:

-   How much does your software development speed suffer because of
    incorrect comments?
-   How much does your software development speed suffer because of
    missing comments?

For me the cost of missing comments is easily 10-100x the cost of incorrect
comments. That is why I cringe when I see things in _Clean Code_ that
discourage people from writing comments.

Let's consider the `PrimeGenerator` class. There is not a single comment
in that code; does this seem appropriate to you?

### UB

I think it was appropriate for the purpose for which I wrote it. It was an adjunct to the lesson that very large methods can be broken down into smaller classes containing smaller methods. Adding lots of explanatory comments would have detracted from that point.

In general, however, the commenting style I used in Listing 4-8 is more appropriate. That listing, at the very end of the _Comments_ chapter, describes yet another `PrimeGenertor` with a slightly different algorithm, and a better set of comments.

### John

I disagree that adding comments would have distracted from your point,
and I think Listing 4-8 is also woefully undercommented.
But let's not argue about either of those issues. Instead, let's discuss
what comments the PrimeGenerator code _should_ have if it were used in production.
I will make some suggestions and you can agree or disagree.

For starters, let's discuss your use of megasyllabic names like
`isLeastRelevantMultipleOfLargerPrimeFactor`. My understanding is that
you advocate using names like this instead of using shorter names
augmented with descriptive comments: you're effectively moving the
comments into code. To me, this approach is problematic:

-   Long names are awkward. Developers effectively have to retype
    the documentation for a method every time they invoke it, and the long
    names waste horizontal space and trigger line wraps in the code. The names are
    also awkward to read: my mind wants to parse every syllable every time
    I read it, which slows me down. Notice that both you and I resorted to
    abbreviating names in this discussion: that's an indication that
    the long names are awkward and unhepful.
-   The names are hard to parse and don't convey information as effectively
    as a comment.
    When students read `PrimeGenerator` one of the first things they
    complain about is the long names (students can't make sense of them).
    For example, the name above is
    vague and cryptic: what does "least relevant" mean, and what is a
    "larger prime factor"? Even with a complete understanding of the code in
    the method, it's hard for me to make sense of the name. If this name
    is going to eliminate the need for a comment, it needs to be even longer.

In my opinion, the traditional approach of using shorter names with
descriptive comments is more convenient and conveys the required information
more effectively. What advantage is there in the approach you advocate?

### UB

"_Megasyllabic_": Great word!

I like my method names to be sentence fragments that fit nicely with keywords and assignment statements. It makes the code a bit more natural to read.

```java
if (isTooHot)
    cooler.turnOn();
```

I also follow a simple rule about the length of names. The larger the scope of a method, the shorter its name should be and vice-versa -- the shorter the scope the longer the name. The private methods I extracted in this case live in very small scopes, and so have longish names. Methods like this are typically called from only one place, so there is no burden on the programmer to remember a long name for another call.

### John

Names like `isTooHot` are totally fine by me.
My concern is about names like `isLeastRelevantMultipleOfLargerPrimeFactor`.

It's interesting that as methods get smaller and narrower, you recommend
longer names.
What this says to me is that the interfaces for those functions are
more complex, so it takes more words to describe them. This provides
supporting evidence for
my assertion a while back that the more you split up a method,
the shallower the resulting methods will be.

### UB

It's not the functions that get smaller, it's the scope that gets smaller. A private function has a smaller scope than the public function that calls it. A function called by that private function has an even smaller scope. As we descend in scope, we also descend in situational detail. Describing such detail often requires a long name, or a long comment. I prefer to use a name.

As for long names being hard to parse, that's a matter of practice. Code is full of things that take practice to get used to.

### John

I don't accept this. Code may be full of things that take practice to get used
to, but that doesn't excuse it.
Approaches that require more practice are worse than
those that require less.
If it's going to take a lot of work to get comfortable with the long names
then there had better be some compensating benefit; so far I'm not seeing any.
And I don't see any reason to believe that practice will make those names
easier to digest.

In addition, your comment above violates one of my fundamental rules, which
is "complexity is in the eye of the reader". If you write code that someone
else thinks is complicated, then you must accept that the code is probably
complicated (unless you think the reader is completely incompetent). It
is not OK to make excuses or suggest that it is really the reader's problem
("you just don't have enough practice"). I'm going to have to live by this
same rule a bit later in our discussion.

### UB

Fair enough. As for the meaning of "leastRelevant", that's a much larger problem that you and I will encounter shortly. It has to do with the intimacy that the author has with the solution, and the reader's lack of that intimacy.

### John

You still haven't answererd my question: why is it better to use super-long names
rather than shorter names augmented with descriptive comments?

### UB

It's a matter of preference for me. I prefer long names to comments. I don't trust comments to be maintained, nor do I trust that they will be read. Have you ever noticed that many IDEs paint comments in light grey so that they can be easily ignored? It's harder to ignore a name than a comment.

(BTW, I have my IDE paint comments in bright fire-engine red)

### John

I don't see why a monster name is more likely to be "maintained" than
a comment, and I don't agree that IDEs encourage people to ignore
comments (this is your bias coming out again). My current IDE (VSCode)
doesn't use a lighter color for comments.
My previous one (NetBeans) did, but the color scheme didn't hide the comments; it
distinguished them from the code in a way that made both code and comments
easier to read.

Now that we've discussed the specific issue of comments vs. long method
names, let's talk about comments in general. I think there are two major reasons
why comments are needed. The first reason for comments is abstraction.
Simply put, without comments there is no way to have abstraction or modularity.

Abstraction is one of the most important components of good software design.
I define an abstraction as "a simplified way of thinking about something
that omits unimportant details." The most obvious example of an abstraction
is a method. It should be possible to use a method without reading its code.
The way we achieve this is by writing a header comment that describes
the method's _interface_ (all the information someone needs in order
to invoke the method). If the method is well designed, the interface will be
much simpler than the code of the method (it omits implementation details),
so the comments reduce the amount of information people must have in
their heads.

### UB

Long ago, in a 1995 book, I defined abstraction as:

> _The amplification of the essential and the elimination of the irrelevant._

I certainly agree that abstraction is of importance to good software design. I also agree that well placed comments can enhance the ability of readers to understand the abstractions we are attempting to employ. I disagree that comments are the _only_, or even the _best_, way to understand those abstractions. But sometimes they are the only option.

But consider:

```java
addSongToLibrary(String title, String[] authors, int durationInSeconds);
```

This seems like a very nice abstraction to me, and I cannot imagine how a comment might improve it.

### John

Our definitions of abstraction are very similar; that's good to see.
However, the `addSongToLibrary` declaration is not (yet) a good abstraction
because it omits information
that is essential. In order to use `addSongToLibrary`, developers
need answers to the following questions:

-   Is there any expected format for an author string, such as "LastName, FirstName"?
-   Are the authors expected to be in alphabetical order? If not, is the order
    significant in some other way?
-   What happens if there is already a song in the library with the given title
    but different authors? Is it replaced with the new one, or will the library
    keep multiple songs with the same title?
-   How is the library stored (e.g. is it entirely in memory? saved on disk?)?
    If this information is documented somewhere else, such as the
    overall class documentation, then it need not be repeated here.

Thus `addSongToLibrary` needs quite a few comments.
Sometimes the signature of a method (names and types of the method, its
arguments, and its return value) contains all the information
needed to use it, but this is pretty rare. Just skim through the documentation
for your favorite library package: in how many cases could you understand how
to use a method with only its signature?

### UB

Yes, there are times when the signature of a method is an incomplete abstraction and a comment
is required. This is especially true when the interface is part of a public API, or an API intended
for use by a separate team of developers. Within a single development team, however, long descriptive
comments on interfaces are often more of an impediment than a help. The team has intimate knowledge of the
internals of the system, and will generally be able to understand an interface simply from its
signature.

### John

In one of our in-person discussions you argued that interface comments
are unnecessary because when a group of developers is working on a body
of code they can collectively keep the entire code "loaded" in their
minds, so comments are unnecessary: if you have a question, just ask the
person who is familiar with that code. This creates a huge cognitive load
to keep all that code mentally loaded, and it's hard for me to imagine
that it would actually work. Maybe your memory is better than mine, but I
find that I quickly forget code that I wrote just a few weeks ago. In
a project of any size, I think your approach would result in developers
spending large amounts of time reading code to re-derive the interfaces,
and probably making mistakes along the way. Spending a few minutes to
document the interfaces would save time, reduce cognitive load, and
reduce bugs.

### UB

I think that certain interfaces need comments, even if they are private to the team. But I think it is more often the case that the team is familiar enough with the system that well named methods and arguments are sufficient.

### John

Let's consider a specific example from `PrimeGenerator`: the `isMultipleOfNthPrimeFactor`
method. When someone reading the code encounters the call to `isMultiple...`
in `isNot...` they need to understand enough about how `isMultiple...` works
in order to see how it fits into the code of `isNot...`.
The method name does not fully document the interface, so if there
is no header comment then readers will have to read the code of `isMultiple`.
This will force readers to load more information into their
heads, which makes it harder to work in the code.

Here is my first attempt at a header comment for `isMultiple`:

```java
/**
 * Returns true if candidate is a multiple of primes[n], false otherwise.
 * May modify multiplesOfPrimeFactors[n].
 * @param candidate
 *      Number being tested for primality; must be at least as
 *      large as any value passed to this method in the past.
 * @param n
 *      Selects a prime number to test against; must be
 *      <= multiplesOfPrimeFactors.size().
 */
```

What do you think of this?

### UB

I think it's accurate. I wouldn't delete it if I encountered it. I don't think it should be a javadoc.

The first sentence is redundant with the name `isMultipleOfNthPrimeFactor` and so could be deleted. The warning of the side effect is useful.

### John

I agree that the first sentence is largely redundant with the name,
and I debated with myself about whether to keep it. I decided to keep it
because I think it is a bit more precise than the name; it's also easier
to read. You propose to eliminate the redundancy between the comment and
the method name by dropping the comment; I would eliminate the redundancy by
shortening the method name.

By the way, you complained earlier about comments being less precise than
code, but in this case the comment is _more_ precise (the method
name can't include text like `primes[n]`).

### UB

Fair enough. There are times when precision is better expressed in a comment.

Continuing with my critique of your comment above: The name `candidate` is synonymous with "Number being tested for primality".

In the end, however, all the words in a comment are just going to have to sit in my brain
until I understand why they are there. I'm also going to have to worry if
they are accurate. So I'm going to have to read the code to understand and
validate the comment.

### John

Whoah. That loud sound you just heard was my jaw hitting the floor.
Help me understand this a bit better: approximately what
fraction of comments that you encounter in practice are you willing to
trust without reading the code to verify them?

### UB

I look at every comment as potential misinformation. At best they are a way to crosscheck the author's intent against the code. The amount of credence I give to a comment depends a lot on how easy they make that crosscheck. When I read a comment that does not cause me to crosscheck, then I consider it to be of no value. When I see a comment that causes me to crosscheck, and when that crosscheck turns out to be valuable, then that's a really good comment.

Another way to say this is that the best comments tell me something surprising and verifiable about the code. The worst are those that waste my time telling me something obvious, or incorrect.

### John

It sounds like your answer is 0%: you don't trust any comment unless it has
been verified against the code. This makes no sense to me. As I said above, the vast
majority of comments are correct. It's not hard to write comments; the students
in my software design class are doing this pretty well within a few weeks.
It's also not hard to keep comments up to date as code evolves. Your refusal
to trust comments is another sign of your irrational bias against comments.

Refusing to trust comments incurs a very high cost. In order to understand
how to invoke a method, you will have to read all of the code of that method;
if the method invokes other methods, you will
also have to read them, and the methods they invoke, recursively. This is
an enormous amount of work in comparison to reading (and trusting) a
simple interface comment like the one I wrote above.

If you choose not to write an interface comment for methods, then you
leave the interface of that method undefined. Even if someone reads the
code of the method, they won't be able to tell which parts of the
implementation are expected to remain the same and which parts may
change (there is no way to specify this "contract" in code). This will
result in misunderstanding and more bugs.

### UB

Well, I guess I've just been burned more than you have. I've gone down too many false comment induced rabbit holes, and wasted too much time on worthless word salads.

Of course my trust in comments is not a binary thing. I read them if they are there; but
I don't implicitly trust then. The more gratuitous I feel the author was, or the less adept at english the author is, the less I trust the comments.

As I said above, our IDEs tend to paint comments in an ignorable color. I have my IDE paint comments in bright fire engine red because when I write a comment I intend for it to be read.

By the same token I use long names as a subsitute for comments because I intend for those long names to be read; and it is very hard for a programmer to ignore names.

### John

I mentioned earlier that there are two general reasons why comments are
needed. So far we've been discussing the first reason (abstraction).
The second general reason for comments is for important information
that is not obvious from the code. The algorithm in `PrimeGenerator`
is very non-obvious, so quite a few comments are needed to help readers
understand what is going on and why. Most of the algorithm's complexity
arises because it is designed to compute primes efficiently:

-   The algorithm goes out of its way to avoid divisions, which were quite
    expensive when Knuth wrote his original version (they aren't that expensive
    nowadays).

-   The first multiple for each new prime number is computed by squaring the
    prime, rather than multiplying it by 3. This is mysterious: why is it safe
    to skip the intervening odd multiples? Furthermore, it might seem that this
    optimization only has a small impact on performance, but in fact it makes an
    _enormous_ difference (orders of magnitude). Using the square has the
    side-effect that when
    testing a candidate, only primes up to the square root of the
    candidate are tested. If 3x were used as the initial multiple, primes
    within a factor of 3 of the candidate would be tested; that's a _lot_
    more tests.
    This implication of using the square is so non-obvious that I only realized
    it while preparing material for this discussion; it never occurred to me in
    the many times I have discussed the code with students.

Neither of these issues is obvious from the code; without
comments, readers are left to figure them out on their own. The students
in my class are generally unable to figure out either of them in the
30 minutes I give them, but I think that comments would have
allowed them to understand in a few minutes. Going back to my
introductory remarks, this is an example where information is important,
so it needs to be made available.

Do you agree that there should be comments to explain each of these
two issues?

### UB

I agree that the algorithm is subtle. Setting the first prime multiple as the square of the prime was deeply mysterious at first. I had to go on an hour long bike ride to understand it.

Would a comment help? Perhaps. However, my guess is that no one who has been reading our conversation has been helped by it, because you and I are now too intimate with the solution. You and I can talk about that solution using words that fit into that intimacy; but our readers likely do not yet enjoy that fit.

One solution is to paint a picture -- being worth a thousand words. Here's my attempt.

                                                                    X
                                                        1111111111111111111111111
           1111122222333334444455555666667777788888999990000011111222223333344444
       35791357913579135791357913579135791357913579135791357913579135791357913579
       !!! !! !! !  !!  ! !! !  !  !!  ! !!  ! !  !   ! !! !! !
     3 |||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-||-
     5 |||||||||||-||||-||||-||||-||||-||||-||||-||||-||||-||||-||||-
     7 |||||||||||||||||||||||-||||||-||||||-||||||-||||||-||||||-||||||-
    11 |||||||||||||||||||||||||||||||||||||||||||||||||||||||||||-||||||||||-
    13 ||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
    ...
    113||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

I expect that our readers will have to stare at this for some time, and also look at the code. But then there will be a _click_ in their brains and they'll say "Ohhh! Yes! I see it now!"

### John

I found this diagram very hard to understand.
It begs for supplemental English text to explain the ideas being
presented. Even the syntax is non-obvious: what does
`1111111111111111111111111` mean?

Maybe we have a fundamental difference of philosophy here. I get the sense
that you are happy to give readers a few clues and leave it to them to put
the clues together. Perhaps you don't mind if people have to stare at something
for a while to figure it out? I don't agree with this approach: it results
in wasted time, misunderstandings, and bugs.
I think software should be totally _obvious_, where readers don't need to
be clever or "stare at this for some time" to figure things out.
Suffering followed by catharsis is great for Greek tragedies, but not
for reading code. Every question
a reader might have should be naturally answered, either in the code or
in comments. Key ideas and important conclusions should be stated explicitly,
not left for the reader to deduce. Ideally, even if a reader is in a hurry
and doesn't read the code very carefully, their first guesses about how
things work (and why) should be correct. To me, that's clean code.

### UB

I don't disagree with your sentiment. Good clean code should be as easy as possible to understand. I want to give my readers as many clues as possible so that the code is intuitive to read.

That's the goal. As we are about to see, that can be a tough goal to achieve.

### John

In that case, do you still stand by the "picture" you painted above? It doesn't
seem consistent with what you just said. And if you really wanted to give
your readers as many clues as possible, you'd include a lot more comments.

### UB

I stand by the picture as far as it's accuracy is concerned. And I think it
makes a good crosscheck. I have no illusions that it is easy to understand.

This algorithm is challenging and will require work to comprehend. I finally
understood it when I drew this picture in my mind while on that bike ride. When I got home I drew it for real and presented it in hopes that it might help
someone willing to do the work to understand it.

## Comments Summary

### John

Let's wrap up this section of the discussion. Here is my summary of
where we agree and disgree.

-   Our overall views of comments are fundamentally different. I see more
    value in comments than you do, and I believe that they play a fundamental
    and irreplaceable role in system design. You agree that there are places
    where comments are necessary, but that comments don't always make it
    easier to understand code, so you see far fewer places where comments are
    needed.

-   I would probably write 5-10x more lines of comments for a given piece of
    code than you would.

-   I believe that missing comments are a much greater cause of lost
    productivity than erroneous or unhelpful comments;
    you believe that comments are a net negative, as generally practiced:
    bad comments cost more time than good comments save.

-   You view it as problematic that comments are written in English
    rather than a programming language. I don't see this as particularly
    problematic and think that in many cases English works better.

-   You recommend that developers should take information that I would
    represent as comments and recast it into code if at all possible. One
    example of this is super-long method names. I believe that super-long names
    are awkward and hard to understand, and that it would be better to use
    shorter names supplemented with comments.

-   I believe that it is not possible to define interfaces and create
    abstractions without a lot of comments. You agree for public APIs, but see little need to comment
    interfaces that are internal to the team.

-   You are unwilling to trust comments until you have read code to
    verify them. I generally trust comments; by doing so, I don't need to read
    as much code as you do. You think this exposes me to too much risk.

-   We agree that implementation code only needs comments when the code is
    nonobvious. Although neither of us argues for a large number of implementation
    comments, I'm more likely to see value in them than you do.

Overall, we struggled to find areas of agreement on this topic.

### UB

This is a fair assessment of our individual positions; which I assume are based on our
different individual experiences. Over the years I have found the vast majority
of comments, as generally practiced in the industry, to be unhelpful. You seem to have found more
help in the comments you have encountered.
