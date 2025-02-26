+++
title = "Test-Driven Development"
weight = 60
+++

### John

Let's move on to our third area of disagreement, which is Test-Driven
Development. I am a huge fan of unit testing. I believe that unit tests are
an indispensable part of the software development process and pay for
themselves over and over. I think we agree on this.

However, I am not fan of Test-Driven Development (TDD), which dictates
that tests must be written before code and that code must be written
and tested in tiny increments. This approach has serious problems
without any compensating advantages that I have been able to identify.

### UB

As I said at the start I have carefully read _A Philosophy of Software Design_. I found it to be full of worthwhile insights, and I strongly agree with most of the points you make.

So I was surprised to find, on page 157, that you wrote a very short, dismissive, pejorative, and inaccurate section on _Test Driven Development_. Sorry for all the adjectives, but I think that's a fair characterization. So my goal, here, is to correct the misconceptions that led you to write the following:

> "Test-driven development is an approach to software development where programmers write unit tests before they write code. When creating a new class, the developer first writes unit tests for the class, based on its expected behavior. None of these tests pass, since there is no code for the class. Then the developer works through the tests one at a time, writing enough code for that test to pass. When all of the tests pass, the class is finished."

This is just wrong. TDD is quite considerably different from what you describe. I describe it using three laws.

1.  You are not allowed to write any production code until you have first written a unit test that fails because that code does not exist.

2.  You are not allowed to write more of a unit test than is sufficient to fail, and failing to compile is failing.

3.  You are not allowed to write more production code than is sufficient to make the currently failing test pass.

A little thought will convince you that these three laws will lock you into a cycle that is just a few seconds long. You'll write a line or two of a test that will fail, you'll write a line or two of production code that will pass, around and around every few seconds.

A second layer of TDD is the Red-Green-Refactor loop. This loop is several minutes long. It is comprised of a few cycles of the three laws, followed by a period of reflection and refactoring. During that reflection we pull back from the intimacy of the quick cycle and look at the design of the code we've just written. Is it clean? Is it well structured? Is there a better approach? Does it match the design we are pursuing? If not, should it?

### John

Oops! I plead "guilty as charged" to inaccurately describing TDD.
I will fix this in the next revision of APOSD. That said, your definition
of TDD does not change my concerns.

Let's discuss the potential advantages and disadvantages
of TDD; then readers can decide for themselves whether they think TDD is a
good idea overall.

Before we start that discussion, let me clarify the approach I prefer as an
alternative to TDD. In your online videos you describe the alternative to
TDD as one where a developer writes the code, gets it fully working
(presumably with manual tests), then goes back and writes the unit tests.
You argue that this approach would be terrible: developers
lose interest once they think code is working, so they wouldn't actually
write the tests. I agree with you completely. However, this isn't the only
alternative to TDD.

The approach I prefer is one where the developer works in somewhat
larger units than in TDD, perhaps a few methods or a class. The developer
first writes some code (anywhere from a few tens of lines to a few hundred
lines), then writes unit tests for that code. As with TDD, the
code isn't considered to be "working" until it has comprehensive unit
tests.

### UB

How about if we call this technique "bundling" for purposes of this
document? This is the term I use in _Clean Code 2d ed._

### John

Fine by me.

The reason for working in larger units is to encourage design
thinking, so that a developer can think about a collection of related
tasks and do a bit of planning to come up with a good overall design
where the pieces fit together well.
Of course the initial design ideas will have flaws and refactoring
will still be necessary, but the goal is to center the development
process around design, not tests.

To start our discussion, can you make a list of the advantages you
think that TDD provides over the approach I just described?

### UB

The advantages I usually attribute to TDD are:

-   Very little need for debugging. After all, if you just saw everything working a minute or two ago, there's not much to debug.

-   A stream of reliable low level documentation, in the form of very small and isolated unit tests. Those tests describe the low level structure and operation of every facet of the system. If you want to know how to do something in the system, there are tests that will show you how.

-   A less coupled design which results from the fact that every small part of the system must be designed to be testable, and testability requires decoupling.

-   A suite of tests that you trust with your life, and therefore supports fearless refactoring.

However, you asked me which of these advantages TDD might have over _your_ preferred method. That depends on how big you make those larger units you described. The important thing to me is to keep the cycle time short, and to prevent entanglements that block testability.

It seems to me that working in small units, and then immediately writing after the fact tests, can give you all the above advantages, so long as you are very careful to test every aspect of the code you just wrote. I think a disciplined programmer could effectively work that way. Indeed, I think such a programmer would produce code that I could not distinguish from code written by another programmer following TDD.

Above you suggested that bundling is to encourage design. I think encouraging design is a very good thing. My question for you is: Why do you think that TDD does not encourage design? My own experience is that design comes from strategic thought, which is independent of the tactical behavior of either TDD or Bundling. Design is taking one step back from the code and envisioning structures that address a larger set of constraints and needs.

Once you have that vision in your head it seems to me bundling and TDD will yield similar results.

### John

First, let me address the four advantages you listed for TDD:

-   Very little need for debugging? I think any form of unit testing can
    reduce debugging work, but not for the reason you
    suggested. The benefit comes because unit tests expose bugs earlier
    and in an environment where they are easier to track down. A
    relatively simple bug to fix in development can be very painful to
    track down in production. I'm not convinced by your argument that
    there's less debugging because "you just saw everything working a
    minute ago": it's easy to make a tiny change that exposes a really
    gnarly bug that has existed for a long time but hasn't yet been
    triggered. Hard-to-debug problems arise from the accumulated complexity
    of the system, not from the size of the code increments.

    > **UB**: True. However, when the cycles are very short then the cause
    > of even the gnarliest of bugs have the best chance of being tracked down.
    > The shorter the cycles, the better the chances.

    > **John**: This is only true up to a point. I think you believe
    > that making units smaller and smaller continues to provide benefits,
    > with almost no limit to how small they can get. I think that there
    > is a point of diminishing returns, where making things even smaller
    > no longer helps and actually starts to hurt. We saw this disagreement
    > over method length, and I think we're seeing it again here.

-   Low level documentation? I disagree: unit tests are a poor form
    of documentation. Comments are a much more
    effective form of documentation, and you can put them right next to the
    relevant code. Trying to learn a method's
    interface by reading a bunch of unit tests seems much more difficult
    than just reading a couple of sentences of English text.

    > **UB**: Nowadays it's very easy to find the tests for
    > a function by using the "where-used" feature of the IDE. As for comments
    > being better, if that were true then no one would publish example code.

-   A less coupled design? Possibly, but I haven't experienced this myself.
    It's not clear to me that designing for testability will produce the
    best design.

    > **UB**: Generally the decoupling arises because the test requires a mock
    > of some kind. Mocks tend to force abstractions that might otherwise not exist.

    > **John**: In my experience, mocking virtually never changes interfaces;
    > it just provides replacements for existing (typically immovable)
    > interfaces.

    > **UB**: Our experiences differ.

-   Enabling fearless refactoring? BINGO! This is the where almost all of the
    benefits from unit testing come from, and it is a really really big deal.

    > **UB**: Agreed.

I agree with your conclusion that TDD and bundling are about the
same in terms of providing these benefits.

Now let me explain why I think TDD is likely to result in bad designs.
The fundamental problem with TDD is that it forces developers to work
too tactically, in
units of development that are too small; it discourages design
thinking. With TDD the basic unit of
development is one test: first the test is written, then the code to
make that test pass. However, the natural units for design are larger
than this: a class or method, for example. These units
correspond to multiple test cases. If a developer thinks only about
the next test, they are only considering part of a design problem at
any given time. It's hard to design something well if you don't think
about the whole design problem at once. TDD explicitly
prohibits developers from writing more code than is needed to pass
the current test; this discourages the kind of strategic thinking needed
for good design.

TDD does not provide adequate guidance to encourage design. You mentioned
the Red-Green-Refactor loop, which recommends refactoring after each step,
but there's almost no guidance for refactoring. How should developers
decide when and what to refactor? This seems to be left purely to their
own judgment. For example, if I am writing a method that requires
multiple iterations of the TDD loop, should I refactor after every iteration
(which sounds pretty tedious) or wait until after several iterations so that
I can look at a bigger chunk of code when refactoring and hence be more
strategic? Without guidance it will be tempting for developers to keep
putting off refactoring.

TDD is similar to the One Thing Rule we discsused earlier in that it is
biased: it provides very strong and clear instructions pushing developers
in one direction (in this case, acting tactically) with only vague
guidance in the other direction (designing more strategically). As a result,
developers are likely to err on the side of being too tactical.

TDD guarantees that developers will initially write bad code. If you start
writing code without thinking about the whole design problem, the first code
you write will almost certainly be wrong. Design only
happens after a bunch of bad code has accumulated.
I watched your video on TDD, and
you repeatedly wrote the wrong code, then fixed it later. If the developer
refactors conscientiously (as you did) they can still end up with good
code, but this works against human nature. With TDD, that bad code will
actually work (there are tests to prove it!) and it's human nature not
to want to change something that
works. If the code I'm developing is nontrivial, I will probably have to
accumulate a lot of bad code with TDD before I have enough code in front
of me to understand what the design should have been.
It will be very difficult for me to force myself to throw away
all that work.

It's easy for a developer to believe they are doing TDD correctly while
working entirely tactically, layering on hack after hack with an
occasional minor refactor, without ever thinking about the overall design.

I believe that the bundling approach is superior to TDD because it focuses
the development process around design: design first, then code, then write
unit tests. Of course, refactoring will still be
required: it's almost never possible to get the design right the first time.
But starting with design will reduce the amount of bad code you write and
get you to a good design sooner. It is possible to produce equally good
designs with TDD; it's just harder and requires a lot more discipline.

### UB

I'll address your points one at a time.

-   I haven't found that the scale of TDD is so tactical that it discourages thinking. Every programmer, regardless of their testing discipline, writes code one line at a time. That's immensely tactical and yet does not discourage design. So why would one test at a time discourage it?

-   The literature on TDD strongly discourages delaying refactoring. While thinking about design is strongly encouraged. Both are integral parts of the discipline..

-   We all write bad code at the start. The discipline of TDD gives us the opportunity, and the safety, to continuously clean it. Design insights arise from those kinds of cleaning activities. The discipline of refactoring allows bad designs to be transformed, one step at a time, into better designs.

-   It's not clear to me why the act of writing tests late is a better design choice. There's nothing in TDD that prevents me from thinking through a design long before I write the very first tested code.

### John

You say there is nothing about TDD that stops developers from thinking ahead
about design. This is only partly true. Under TDD I can think ahead, but I
can't actually write my ideas down in the form of code, since that would
violate TDD Rule 1. This is a significant discouragement.

You claim that "thinking about design is strongly encouraged" in TDD,
but I haven't seen this in your discussions of TDD. I watched your
video example of using TDD
for computing bowling scores, and design is never even mentioned after the
first minute or two (ironically, one of the conclusions of this
example is that the brief initial design turned out to be
useless). There is no suggestion of thinking ahead in the video;
it's all about cleaning up messes after the fact.
In all of the TDD materials you have shown me, I have not seen any
warnings about the dangers of becoming so tactical with TDD that
design never occurs (perhaps you don't even view this as a serious risk?).

### UB

I usually use an abbeviated form of UML to capture my early design decisions. I have no objection to capturing them in pseudo-code, or even real code. However, I would not commit any such pre-written code. I would likely hold it in a text file, and consult it while following the TDD cycle. I might feel safe enough to copy and paste from the text file into my IDE in order to make a failing test pass.

The Bowling game is an example of how wildly our initial design decisions can deviate from our eventual solutions. It's true that introductory videos often do not expose the depth of a discipline.

### John

As I was watching your TDD video for the second time, you said something
that jumped out at me:

> Humans consider things that come first to be important and things that
> come at the end to be less important and somehow optional; that's
> why they are at the end, so we can leave them out if we have to.

This captures perfectly my concern about TDD. TDD insists that tests must
come first, and design, if it happens at all, comes at the end, after
code is working. I believe that good design is the most important
thing, so it must be the top priority. I don't consider tests optional,
but delaying them is safer than delaying design. Writing tests isn't particularly
difficult; the most important thing is having the discipline to do it.
Getting a good design is really hard, even if you are very disciplined;
that's why it needs to be the center of attention.

### UB

TDD is a coding discipline. Of course design comes before coding -- I don't know anyone who thinks otherwise. Even the Bowling Game video made that point. But, as we saw in the Bowling Game video, sometimes the code will take you in a very different direction.

That difference does't imply that the design shouldn't have been done. It just implies that designs are speculative and may not aways survive reality.

As Eisenhower once said:

> “In preparing for battle I have always found that plans are useless, but planning is indispensable.”

### John

You ask why writing tests later is a better design choice. It isn't.
The benefit of the bundled approach doesn't come from writing tests later;
it comes from doing design sooner. Writing tests (a bit) later is a
consequence of this choice. The tests are still written pretty early-on
with the bundled approach, so I don't think the delay causes significant
problems.

### UB

I think we simply disagree that TDD discourages design. The practice of TDD does not discourage me from design; because I value design. I would suggest that those who do not value design will not design, no matter what discipline they practice.

### John

You claim that the problems I worry about with TDD simply don't happen in
practice. Unfortunately I have heard contrary claims from senior
developers that I trust. They complain about horrible code produced by
TDD-based teams, and they believe that the problems were caused by TDD.
Of course horrible code can be produced with any design approach.
And maybe those teams didn't implement TDD properly, or maybe those
cases were outliers.
But the problems reported to me line up exactly with what I would
expect to happen, given the tactical nature of TDD.

### UB

My experience differs. I've worked on many projects where TDD has been used
effectively and profitably. I'm sure the senior developers that you trust are telling you the truth about their experience. Having never seen TDD lead to such bad outcomes myself, I sincerely doubt that the blame can be traced to TDD.

### John

You ask me to trust your extensive experience with
TDD, and I admit that I have no personal experience with TDD.
On the other hand, I have a lot of experience with tactical programming,
and I know that it rarely ends well.
TDD is one of the most extreme forms of tactical programming I've
encountered.
In general, if "making it work" is the #1 prority, instead of
"develop a clean design", code turns to spaghetti.
I don't see enough safeguards in your approach to TDD
to prevent the disaster scenarios; I don't even see a clear
recognition of the risk.

Overall, TDD is in a bad place on the risk-reward spectrum. In comparison
to the bundling approach, the downside risks for poor code quality in TDD
are huge, and I don't see enough upside reward (if any) to compensate.

### UB

All I can say to that is that your opinion is based on a number of false impressions and speculations, and not upon direct experience.

### John

Now let me ask you a couple of questions.

First, at a microscopic level, why on earth does TDD prohibit developers
from writing more code than needed to pass the current test? How does
enforcing myopia make systems better?

> **UB**:
> The goal of the discipline is to make sure that everything is tested.
> One good way to do that is to refuse to write any code unless it is to make a failing test pass. Also, working in such short cycles provides insights into
> the way the code is working. Those insights often lead to better design decisions.

> **John**:
> I agree that seeing code (partially) working can provide insights. But
> surely that benefit can be had without such a severe restriction on
> how developers think?

Second, at a broader level, do you think TDD is likely to produce better
designs than approaches that are more design-centric, such as the bundling
approach I described? If so, can you explain why?

> **UB**:
> My guess is that someone adept at bundling, and someone adept at TDD would produce very similar designs, with very similar test coverage. I would also venture to guess that the TDDer would be somewhat more productive than the bundler if for no reason other than that the TDDer finds and fixes problems earlier than the bundler.

> **John**:
> I think that the bundling approach will result in a better design because
> it actually focuses on design, rather than focusing on tests and hoping
> that a good design will magically emerge. I think it's really hard to argue
> that the best way to achieve one thing is to focus your attention on
> something else. And the bundling approach will
> make progress faster because the early thinking about design will reduce the
> amount of bad code you end up having to throw away under TDD. Overall, I'd
> argue that the best-case outcomes for the two approaches will
> be about the same, but average and (especially) worst-case outcomes will
> be far worse for TDD.

### John

I don't think we're going to resolve our disagreements on TDD.
To do that, we'd need empirical data about the frequency of good and bad
outcomes from TDD. Unfortunately I'm not aware of any such data.
Thus, readers will have to decide for themselves whether the potential
benefits of TDD outweigh the risks.

For anyone who chooses to use TDD, I urge you to do so with extreme
caution. Your primary goal must not be just working code, but rather a
clean design that will allow you to develop quickly in the future.
TDD will not lead you naturally to the best design, so you will need
to do significant and continuous refactoring to avoid spaghetti code.
Ask yourself repeatedly "suppose that I knew everything I know now when
I first started on this project; would I have chosen the current
structure for the code?" When the answer is no (which will happen
frequently) stop and refactor. Recognize that TDD will cause you to
write more bad code than you may be used to, so
you must be prepared to throw out and rewrite more than you are used to.
Take time to plan ahead and think about the overall design, rather than
just making the next test work.
If you do all of these things diligently, I think it is possible to
mitigate the risks of TDD and produce well-designed code.

### UB

Let's just say that I agree with all that advice, but disagree with your assertion that TDD might be the cause of bad code.

## TDD Summary

### John

Here is my attempt to summarize our thoughts on Test-Driven Development:

-   We agree that unit tests are an essential element in software development.
    They allow developers to make significant changes to a system without fear
    of breaking something.

-   We agree that it is possible use TDD to produce systems with good designs.

-   I believe that TDD discourages good design and can easily lead to very bad
    code. You do not believe that TDD discourages good
    design and don't see much of a risk of bad code.

-   I believe that there are better approaches than TDD for producing good
    unit test suites, such as the "bundling" approach discussed above. You agree
    that bundling can produce outcomes just as good as TDD but think it may lead to
    somewhat less test coverage.

-   I believe that TDD and bundling have similar best-case outcomes, but that
    the average and worst-case outcomes will be much worse for TDD. You disagree
    and believe that, if anything, TDD may produce marginally better outcomes
    than bundling. You also think that preference and personality are larger factors in
    making the choice between the two.

### UB

This is a fair summary of our discussion. We seem to disagree over the best application
of discipline. I prefer a disciplined approach to keep the code covered by tests
written first in very short cycles. You prefer a disciplined approach of writing relatively longer
bundles of code and then writing tests for those bundles. We disagree on the risks and rewards of
these two disciplines.
