+++
title = "Closing Remarks"
weight = 70
no_prev = false
no_next = true
+++

### John

First, I'd like to thank you for tolerating (and responding to) the arguments
I have made about some of the key ideas in _Clean Code_. I hope this
discussion will provide food for thought for readers.

We have covered a lot of topics and subtopics in this discussion, but
I think that most of my concerns result from two general errors made
by _Clean Code_: failure to focus on what is important, and failure to
balance design tradeoffs.

In software design (and probably in any design environment) it is essential
to identify the things that really matter and focus on those. If you
focus your attention on things that are unimportant you are
unlikely to achieve the things that really are important.
Unfortunately, _Clean Code_ repeatedly focuses on things that don't really
matter, such as:

-   Dividing ten-line methods into five-line methods and dividing five-line methods
    into two- or three-line methods.
-   Eliminating the use of comments written in English.
-   Writing tests before code and making the basic unit of development a
    test rather than an abstraction.

None of these provides significant value, and we have seen how they
distract from producing the best possible designs.

Conversely, _Clean Code_ fundamentally undervalues comments, which are
essential and irreplaceable. This
comes at a huge cost. Without interface comments the specifications for
interfaces are incomplete. This is guaranteed to result in confusion and bugs.
Without implementation comments, readers are forced to rederive knowledge
and intentions that were in the mind of the original developer. This wastes
time and leads to more bugs.

In my opening remarks I said that systems become complex when important
information is not accessible and obvious to developers. By refusing to
write comments, you are hiding important information that you have and
that others need.

The second general error in _Clean Code_ has to do with balance. Design
represents a balance between competing concerns. Almost any design idea
becomes a bad thing if taken to the extreme. However, _Clean Code_
repeatedly gives very strong advice in one direction without correspondingly
strong advice in the other direction or any meaningful guidance about how
to recognize when you have gone too far. For example, making methods
shorter is often a good thing, but the _Clean Code_ position is so one-sided
and extreme that readers are likely to chop things up too much. We saw
in the `PrimeGenerator` example how this resulted in code that was
nearly incomprehensible. Similarly, the _Clean Code_ position on TDD is
one-sided, failing to
recognize any possible weakness and encouraging readers to take this to
a tactical extreme where design is completely squeezed out of the development
process.

### UB

John, I'd like to thank you for participating in this project. This was a lot of fun for me. I love disagreement and debate with smart people. I also think that we share far more values than separate us.

For my part I'll just say that I have given due consideration to the points you've made, and while I disagree with your conclusions above, I have integrated several of your better ideas, as well as this entire document, into the second edition of _Clean Code_.

Thanks again, and give my best to your students.
