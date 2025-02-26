+++
title = "Method Length"
weight = 20
+++

### John

Our first area of disagreement is method length.
On page 34 of _Clean Code_ you say "The first rule of functions is that
they should be small. The second rule of functions is that
_they should be smaller than that_." Later on, you say "Functions
should hardly ever be 20 lines long" and suggest that functions
should be "just two, three, or four lines long". On page 35, you
say "Blocks within `if` statements, `else` statements, `while` statements,
and so on should be one line long. Probably that line should be a function
call." I couldn't find anything in _Clean Code_ to suggest that a function
could ever be too short.

I agree that dividing up code into relatively small units ("modular design")
is one of the most important ways to reduce the amount of information a
programmer has to keep in their mind at once. The idea, of course, is to take a
complex chunk of functionality and encapsulate it in a separate method
with a simple interface. Developers can then harness the functionality
of the method (or read code that invokes the method) without learning
the details of how the method is implemented; they only need to learn its
interface. The best methods are those that provide a lot of functionality
but have a very simple interface: they replace a large cognitive load
(reading the detailed implementation) with a much smaller
cognitive load (learning the interface). I call these methods "deep".

However, like most ideas in software design, decomposition can be taken too far.
As methods get smaller and smaller there is less and less
benefit to further subdivision.
The amount of functionality hidden behind each interface
drops, while the interfaces often become more complex.
I call these interfaces "shallow": they don't help much in terms of
reducing what the programmer needs to know. Eventually, the point is
reached where someone using the method needs
to understand every aspect of its implementation. Such methods
are usually pointless.

Another problem with decomposing too far is that it tends to
result in _entanglement_. Two methods
are entangled (or "conjoined" in APOSD terminology) if, in order to
understand how one of them works internally, you also need to read the
code of the other. If you've ever found yourself flipping back and forth
between the implementations of two methods as you read code, that's a
red flag that the methods might be entangled. Entangled methods
are hard to read because the information you need to have in your head
at once isn't all in the same place. Entangled methods can usually
be improved by combining them so that all the code is in one place.

The advice in _Clean Code_ on method length is so extreme that it encourages
programmers to create teeny-tiny methods that suffer from both shallow
interfaces and entanglement. Setting arbitrary numerical limits such
as 2-4 lines in a method and a single line in the body of an
`if` or `while` statement exacerbates this problem.

### UB

While I do strongly recommend very short functions, I don't think it's fair to say that the book sets arbitrary numerical limits. The 2-4 line functions that you referred to on page 34 were part of the _Sparkle_ applet that Kent Beck and I wrote together in 1999 as an exercise for learning TDD. I thought it was remarkable that most of the functions in that applet were 2-4 lines long because it was a Swing program; and Swing programs tend to have very long methods.

As for setting limits, on page 13 I make clear that although the recommendations in the book have worked well for me and the other authors, they might not work for everyone. I claimed no final authority, nor even any absolute "rightness". They are offered for consideration.

### John

I think these problems will be easiest to understand if we look at
specific code examples. But before we do that, let me ask you, Bob:
do you believe that it's possible for code to be over-decomposed, or
is smaller always better? And, if you believe that over-decomposition
is possible, how do you recognize when it has occurred?

### UB

It is certainly possible to over-decompose code. Here's an example:

```java
void doSomething() {doTheThing()} // over-decomposed.
```

The strategy that I use for deciding how far to take decomposition is the old rule that a method should do "_One Thing_". If I can _meaningfully_ extract one method from another, then the original method did more than one thing. "Meaningfully" means that the extracted functionality can be given a descriptive name; and that it does less than the original method.

### John

Unfortunately the One Thing approach will lead to over-decompositon:

1.  The term "one thing" is vague and easy to abuse. For example, if a method has two lines of code, isn't it doing two things?

2.  You haven't provided any useful guardrails to prevent over-decomposition. The example you gave is too extreme to be useful, and the "can it be named" qualification doesn't help: anything can be named.

3.  The One Thing approach is simply wrong in many cases. If two things are closely related, it might well make sense to implement them in a single method. For example, any thread-safe method will first have to acquire a lock, then carry out its function. These are two "things", but they belong in the same method.

### UB

Let me tackle the last thing first. You suggested that locking the thread, and preforming a critical section should be together in the same method. However, I would be tempted to separate the locking from the critical section.

```java
void concurrentOperation() {
    lock()
    criticalSection();
    unlock()
}
```

This decouples the critical section from the lock and allows it to be called at times when locking isn't necessary (e.g. in single thread mode) or when the a lock has already been set by someone else.

Now, on to the "ease of abuse" argument. I don't consider that to be a significant concern. `If` statements are easy to abuse. `Switch` statements are easy to abuse. Assignment statements are easy to abuse. The fact that something is easy to abuse does not mean that it should be avoided or suppressed. It simply means people should take appropriate care. There will always be this thing called: _judgment_.

So when faced with this snippet of code in a larger method:

```java
...
amountOwed=0;
totalPoints=0;
...
```

It would be poor judgement to extract them as follows, because the extraction is not meaningful. The implementation is not more deeply detailed than the interface.

```java
void clearAmountOwed() {
    amountOwed=0;
}

void clearTotalPoints() {
  totalPoints=0;
}
```

However it may be good judgement to extract them as follows because the interface is abstract, and the implemention has deeper detail.

```java
void clearTotals() {
    amountOwed=0;
    totalPoints=0;
}
```

The latter has a nice descriptive name that is abstract enough to be meaningful without being redundant. And the two lines together are strongly related so as to qualify for doing _one thing_: initialization.

### John

Of course anything can be abused. But the best approaches to design
encourage people to do things the right way and discourage abuse.
Unfortunately, the One Thing Rule encourages abuse for the reasons I
gave above.

And of course software designers will need to use judgment: it isn't
possible to provide precise recipes for software design.
But good judgment requires principles and guidance. The
_Clean Code_ arguments about decomposition, including the One Thing
Rule, are one-sided. They give strong, concrete, quantitative
advice about when to chop things up, with virtually no guidance for
how to tell you've gone too far. All I could find is a 2-sentence
example on page 36 about Listing 3-3 (which is pretty trivial),
buried in the middle of exhortations to "chop, chop, chop".

One of the reasons I use the deep/shallow characterization is that it
captures both sides of the tradeoff; it will tell you when a decomposition
is good and also when decomposition makes things worse.

### UB

You make a good point that I don't talk much, in the book, about how to make the judgement call. Back in 2008 my concern was breaking the habit of the very large functions that were common in those early days of the web. I have been more balanced in the 2d ed.

Still, if I must err, I'd rather err on the side of decomposition. There is value in considering, and visualizing decompositions. They can always be inlined if we judge them to have gone too far.

### John

Coming back to your `clearTotals` example:

-   The `clearTotals` method seems to contradict the One Thing Rule: the
    variables `amountOwed` and `totalPoints` don't seem particularly related, so
    initializing them both is doing two things, no? You say that both
    statements are performing initialization, which makes it just one thing
    (initialization). Does that mean it would also be okay to have a single
    method that initializes two completely independent objects with nothing in
    common? I suspect not. It feels like you are struggling to create a clean
    framework for applying the One Thing Rule; that makes me think it isn't
    a good rule.
-   Without seeing more context I'm skeptical that the `clearTotals`
    method makes sense.

### UB

I hope you agree that between these two examples, the former is a bit better.

```java
public String makeStatement() {
    clearTotals();
    return makeHeader() + makeRentalDetails() + makeFooter();
}
```

---

```java
public String makeStatement() {
    amountOwed=0;
    totalPoints=0;
    return makeHeader() + makeRentalDetails() + makeFooter();
}
```

### John

Well, actually, no. The second example is completely clear and obvious:
I don't see anything to be gained by splitting it up.

### SPOCK (a.k.a UB)

Fascinating.

### John

I think it will be easier to clarify our differences if we consider
a nontrivial code example. Let's look at the `PrimeGenerator` class from
_Clean Code_, which is Listing 10-8 on pages 145-146. This Java class
generates the first N prime numbers:

```java
package literatePrimes;

import java.util.ArrayList;

public class PrimeGenerator {
    private static int[] primes;
    private static ArrayList<Integer> multiplesOfPrimeFactors;

    protected static int[] generate(int n) {
        primes = new int[n];
        multiplesOfPrimeFactors = new ArrayList<Integer>();
        set2AsFirstPrime();
        checkOddNumbersForSubsequentPrimes();
        return primes;
    }

    private static void set2AsFirstPrime() {
        primes[0] = 2;
        multiplesOfPrimeFactors.add(2);
    }

    private static void checkOddNumbersForSubsequentPrimes() {
        int primeIndex = 1;
        for (int candidate = 3; primeIndex < primes.length; candidate += 2) {
            if (isPrime(candidate))
                primes[primeIndex++] = candidate;
        }
    }

    private static boolean isPrime(int candidate) {
        if (isLeastRelevantMultipleOfLargerPrimeFactor(candidate)) {
            multiplesOfPrimeFactors.add(candidate);
            return false;
        }
        return isNotMultipleOfAnyPreviousPrimeFactor(candidate);
    }

    private static boolean isLeastRelevantMultipleOfLargerPrimeFactor(int candidate) {
        int nextLargerPrimeFactor = primes[multiplesOfPrimeFactors.size()];
        int leastRelevantMultiple = nextLargerPrimeFactor * nextLargerPrimeFactor;
        return candidate == leastRelevantMultiple;
    }

    private static boolean isNotMultipleOfAnyPreviousPrimeFactor(int candidate) {
        for (int n = 1; n < multiplesOfPrimeFactors.size(); n++) {
            if (isMultipleOfNthPrimeFactor(candidate, n))
                return false;
        }
        return true;
    }

    private static boolean isMultipleOfNthPrimeFactor(int candidate, int n) {
        return candidate == smallestOddNthMultipleNotLessThanCandidate(candidate, n);
    }

    private static int smallestOddNthMultipleNotLessThanCandidate(int candidate, int n) {
        int multiple = multiplesOfPrimeFactors.get(n);
        while (multiple < candidate)
            multiple += 2 * primes[n];
        multiplesOfPrimeFactors.set(n, multiple);
        return multiple;
    }
}
```

Before we dive into this code, I'd encourage everyone reading
this article to take time to read over the code and draw your own conclusions
about it. Did you find the code easy to understand? If so, why? If not, what
makes it complex?

Also, Bob, can you confirm that you stand by this code (i.e. the code
properly exemplifies the design philosophy of _Clean Code_ and this
is the way you believe the code should appear if it were used in
production)?

### UB

Ah, yes. The `PrimeGenerator`. This code comes from the 1982 paper on [_Literate Programming_](https://www.cs.tufts.edu/~nr/cs257/archive/literate-programming/01-knuth-lp.pdf) written by Donald Knuth. The program was originally written in Pascal, and was automatically generated by Knuth's WEB system into a single very large method which I translated into Java.

Of course this code was never meant for production. Both Knuth and I used it as a pedagogical example. In _Clean Code_ it appears in a chapter named _Classes_. The lesson of the chapter is that a very large method will often contain many different sections of code that are better decomposed into independent classes.

In the chapter I extracted three classes from that function: `PrimePrinter`, `RowColumnPagePrinter` and `PrimeGenerator`.

One of those extracted classes was the `PrimeGenerator`. It had the following code (which I did not publish in the book.) The variable names and the overall structure are Knuth's.

```java
public class PrimeGenerator {
    protected static int[] generate(int n) {
        int[] p = new int[n];
        ArrayList<Integer> mult = new ArrayList<Integer>();
        p[0] = 2;
        mult.add(2);
        int k = 1;
        for (int j = 3; k < p.length; j += 2) {
            boolean jprime = false;
            int ord = mult.size();
            int square = p[ord] * p[ord];
            if (j == square) {
	            mult.add(j);
            } else {
                jprime=true;
                for (int mi = 1; mi < ord; mi++) {
                    int m = mult.get(mi);
                    while (m < j)
                        m += 2 * p[mi];
                    mult.set(mi, m);
                    if (j == m) {
                        jprime = false;
                        break;
                    }
                }
            }
            if (jprime)
                p[k++] = j;
        }
        return p;
    }
}
```

Even though I was done with the lesson of the chapter, I didn't want to leave that method looking so outdated. So I cleaned it up a bit as an afterthought. My goal was not to describe how to generate prime numbers. I wanted my readers to see how large methods, that violate the Single Responsibility Principle, can be broken down into a few smaller well-named classes containing a few smaller well-named methods.

### John

Thanks for the background. Even though the details of that code weren't
the main point of the chapter, presumably the code represents what you think
is the "right" and "cleanest" way to do things, given the algorithm at hand.
And that's where I disagree.

There are many design problems with `PrimeGenerator`, but for now I'll
focus on method length. The code is chopped up so much (8 teeny-tiny methods)
that it's difficult to read. For starters, consider the
`isNotMultipleOfAnyPreviousPrimeFactor` method. This method invokes
`isMultipleOfNthPrimeFactor`, which invokes
`smallestOddNthMultipleNotLessThanCandidate`. These methods are shallow
and entangled:
in order to understand
`isNot...` you have to read the other two
methods and load all of that code into your mind at once. For example,
`isNot...` has side effects (it modifies `multiplesOfPrimeFactors`) but
you can't see that unless you read all three methods.

### UB

I think you have a point. Eighteen years ago, when I was in the throes of this refactoring, the names and structure made perfect sense to me. They make sense to me now, too -- but that's because I once again understand the algorithm. When I returned to the algorithm for the first time a few days ago, I struggled with the names and structure. Once I understood the algorithm the names and structure made perfect sense.

### John

Those names are problematic even for someone who understands the algorithm;
we'll talk about them a bit later, when discussing comments. And, if code
no longer makes sense to the writer when the writer returns to the code later,
that means the code is problematic. The fact that code can eventually
be understood (with great pain and suffering) does not excuse its entanglement.

### UB

Would that we had such a crystal ball that we could help our future selves avoid such "_great pain and suffering_". ;-)

### John

There is no need for a crystal ball. The problems with `PrimeGenerator` are
pretty obvious, such as the entanglement and interface complexity; maybe you
were surprised that it is hard to understand, but I am not. Said another
way, if you are unable to predict whether your code will be easy to
understand, there are problems with your design methodology.

### UB

Fair enough. I will say, however, that I had equal "_pain and suffering_" interpreting your rewrite (below). So, apparently, neither of our methodologies were sufficient to rescue our readers from such struggles.

### John

Going back to my introductory remarks about complexity, splitting up
`isNot...` into three methods doesn't reduce the amount of information
you have to keep in your mind. It just spreads it out, so it isn't as
obvious that you need to read all three methods together. And, it's harder
to see the overall structure of the code because it's split up: readers have
to flip back and forth between the methods, effectively reconstructing a
monolithic version in their minds. Because the pieces are all related,
this code will be easiest to understand if it's all together in one place.

### UB

I disagree. Here is `isNotMultipleOfAnyPreviousPrimeFactor`.

```java
private static boolean isNotMultipleOfAnyPreviousPrimeFactor(int candidate) {
    for (int n = 1; n < multiplesOfPrimeFactors.size(); n++) {
        if (isMultipleOfNthPrimeFactor(candidate, n))
            return false;
    }
    return true;
}
```

If you trust the `isMultipleOfNthPrimeFactor` method, then this method stands alone quite nicely. I mean we loop through all n previous primes and see if the candidate is a multiple. That's pretty straight forward.

Now it would be fair to ask the question how we determine whether the candidate is a multiple, and in that case you'd want to inspect the `isMultiple...` method.

### John

This code does appear to be simple and obvious.
Unfortunately, this appearance is deceiving.
If a reader trusts the name `isMultipleOfNthPrimeFactor` (which suggests
a predicate with no side effects) and doesn't bother to read its code, they
will not realize that it has side effects, and that the side effects
create a constraint on the `candidate` argument to `isNot...`
(it must be monotonically non-decreasing from invocation
to invocation). To understand these behaviors, you have to
read both `isMultiple...` and `smallestOdd...`. The current decomposition
hides this important information from the reader.

If there is one thing more likely to result in bugs than not understanding code,
it's thinking you understand it when you don't.

### UB

That's a valid concern. However, it is tempered by the fact that the functions are presented in the order they are called. Thus we can expect that the reader has already seen the main loop and understands that `candidate` increases by two each iteration.

The side effect buried down in `smallestOddNth...` is a bit more problematic. Now that you've pointed it out I don't like it much. Still, that side effect should not confound the basic understanding of `isNot...`.

In general, if you trust the names of the methods being called then understanding the caller does not require understanding the callee. For example:

```java
for (Employee e : employees)
    if (e.shouldPayToday())
        e.pay();
```

This would not be made more understandable if we replaced those two method calls with the their implementations. Such a replacement would simply obscure the intent.

### John

This example works because the called methods are relatively independent of
the parent. Unfortunately that is not the case for `isNot...`.

In fact, `isNot...` is not only entangled with the methods it calls, it's also
entangled with its callers. `isNot...` only works if it is invoked in
a loop where `candidate` increases monotonically. To convince yourself
that it works, you have to find the code that invokes `isNot...` and
make sure that `candidate` never decreases from one call to the next.
Separating `isNot...` from the loop that invokes it makes it harder
for readers to convince themselves that it works.

### UB

Which, as I said before, is why the methods are ordered the way they are. I expect that by the time you get to `isNot...` you've already read `checkOddNumbersForSubsequentPrimes` and know that `candidate` increases by twos.

### John

Let's discuss this briefly, because it's another area where I
disagree with _Clean Code_. If methods are entangled, there is no
clever ordering of the method definitions that will fix the problem.

In this particular situation two other methods intervene between the
loop in `checkOdd...` and `isNot...`, so readers will have forgotten
the loop context before they get to `isNot...`. Furthermore, the actual
code that creates a dependency on the loop isn't in `isNot...`: it's in
`smallestOdd...`, which is even farther away from `checkOdd...`.

### UB

I sincerely doubt anyone is going to forget that `candidate` is being increased by twos. It's a pretty obvious way to avoid waste.

### John

In my opening remarks I talked about how it's important to reduce the
amount of information people have to keep in their minds at once.
In this situation, readers have to remember that loop while they read
four intervening methods that are mostly unrelated to the loop. You apparently think
this will be easy and natural (I disagree). But it's even worse than
that. There is no indication which parts of `checkOdd...` will be important
later on, so the only safe approach is to remember _everything_, from _every_
method, until you have encountered every other method that could possibly
descend from it. And, to make the connection between the pieces, readers
must also reconstruct the call graph to notice that, even through
4 layers of method call, the code in `smallestOdd...` places constraints
on the loop in `checkOdd...`. This is an unreasonable cognitive burden to
place on readers.

If two pieces of code are tightly related, the solution is to bring
them together. Separating the pieces, even in physically adjacent methods,
makes the code harder to understand.

To me, all of the methods in `PrimeGenerator` are entangled: in order to
understand the class I had to load all of them into my mind
at once. I was constantly flipping back and forth between the methods
as I read the code. This is a red flag indicating
that the code has been over-decomposed.

Bob, can you help me understand why you divided the code into such
tiny methods?
Is there some benefit to having so many methods that I have missed?

### UB

I think you and I are just going to disagree on this. In general I believe in the principle of small well-named methods and the separation of concerns. Generally speaking if you can break a large method into several well-named smaller methods with different concerns, and by doing so expose their interfaces, and the high level functional decomposition, then that's a good thing.

-   Looping over the odd numbers is one concern.
-   Determining primality is another.
-   Marking off the multiples of primes is yet another.

It seems to me that separating and naming those concerns helps to expose the way the algorithm works -- even at the expense of some entaglement.

In your solution, which we are soon to see below, you break the algorithm up in a similar way. However, instead of separating the concerns into functions, you separate them into sections with comments above them.

You mentioned that in my solution readers will have to keep the loop context in mind while reading the other functions. I suggest that in your solution, readers will have to keep the loop context in mind while reading your explanatory comments. They may have to "flip back and forth" between the sections in order to establish their understanding.

Now perhaps you are concerned that in my solution the "flipping" is a longer distance (in lines) than in yours. I'm not sure that's a significant point since they all fit on the same screen (at least they do on my screen) and the landmarks are pretty obvious.

## Method Length Summary

### John

It sounds like it's time to wrap up this section. Is this a reasonable
summary of where we agree and disagree?

-   We agree that modular design is a good thing.

-   We agree that it is possible to over-decompose, and that _Clean Code 1st ed._
    doesn't provide much guidance on how to recognize over-decomposition.

-   We disagree on how far to decompose: you recommend decomposing
    code into much smaller units than I do. You believe that
    the additional decomposition you recommend makes code easier to
    understand; I believe that it goes too far and actually makes code
    more difficult to understand.

-   You believe that the One Thing Rule, applied with judgment, will
    lead to appropriate decompositions. I believe it lacks guardrails
    and will lead to over-decomposition.

-   We agree that the internal decomposition of `PrimeGenerator` into
    methods is problematic. You point out that your main goal in writing
    `PrimeGenerator` was to show how to decompose into classes, not
    so much how to decompose a class internally into methods.

-   Entanglement between methods in a class doesn't bother you
    as much as it bothers me. You believe that the benefits of decomposing
    methods can compensate for problems caused by entanglement.
    I believe they can't: when decomposed methods are entangled,
    they are harder to read than if they were not decomposed, and this
    defeats the whole purpose of decomposition.

-   You believe that ordering the methods in a class can help to
    compensate for entanglement between methods; I don't.

### UB

I think this is a fair assessment of our agreements and disagreements. We both value decomposition,
and we both avoid entanglement; but we disagree on the relative weighting of those two values.
