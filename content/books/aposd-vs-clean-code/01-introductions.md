+++
title = "Introductions"
weight = 10
no_prev = true
no_next = false
+++

### John

Hi (Uncle) Bob! You and I have each written books on software design.
We agree on some things, but there are some pretty big differences of
opinion between my recent book _A Philosophy of Software Design_
(hereafter "APOSD") and your classic book _Clean Code_. Thanks for
agreeing to discuss those differences here.

### UB

My pleasure John. Before we begin let me say that I've carefully read through your book and I found it very enjoyable, and full of valuable insights. There are some things I disagree with you on, such as TDD, and Abstraction-First incrementalism, but overall I enjoyed it a lot.

### John

I'd like to discuss three topics with you: method length, comments,
and test-driven development. But before getting into these,
let's start by comparing overall philosophies. When you hear about a
new idea related to software design, how do you decide whether or not
to endorse that idea?

I'll go first. For me, the fundamental goal of software design is
to make it easy to understand and modify the system. I use the term
"complexity" to refer to things that make it hard to understand and
modify a system. The most important contributors
to complexity relate to information:

-   How much information must a developer have in their head in order to carry out a task?
-   How accessible and obvious is the information that the developer needs?

The more information a developer needs to have, the harder it will be
for them to work on the system. Things get even worse if the required
information isn't obvious. The worst case is when there is a crucial
piece of information hidden in some far-away piece of code
that the developer has never heard of.

When I'm evaluating an idea related to software design, I ask whether
it will reduce complexity. This usually means either reducing the amount
of information a developer has to know, or making the required information
more obvious.

Now over to you: are there general principles that you use when deciding
which ideas to endorse?

### UB

I agree with your approach. A discipline or technique should make the job of programmers easier. I would add that the programmer we want to help most is not the author. The programmer whose job we want to make easier is the programmer who must read and understand the code written by others (or by themself a week later). Programmers spend far more hours reading code than writing code, so the activity we want to ease is that of reading.
