+++
title = "Bob's Rewrite of PrimeGenerator2"
weight = 50
+++

### UB

When I saw your solution, and after I gained a good understanding of it. I refactored it just a bit. I loaded it into my IDE, wrote some simple tests, and extracted a few simple methods.

I also got rid of that _awful_ labeled `continue` statement. And I added 3 to the primes list so that I could mark the first element as _irrelevant_ and give it a value of -1. (I think I was still reeling from the even/odd confusion.)

I like this because the implementation of the `generateFirstNPrimes` method describes the moving parts in a way that hints at what is going on. It's easy to read that implementation and get a glimpse of the mechanism. I'm not at all sure that the comment helps.

I think it is just the reality of this algorithm that the effort required to properly explain it, and the effort required for anyone else to read and understand that explanation is roughly equivalent to the effort needed to read the code and go on a bike ride.

```java
package literatePrimes;

public class PrimeGenerator3 {
    private static int[] primes;
    private static int[] primeMultiples;
    private static int lastRelevantMultiple;
    private static int primesFound;
    private static int candidate;

    // Lovely little algorithm that finds primes by predicting
    // the next composite number and skipping over it. That prediction
    // consists of a set of prime multiples that are continuously
    // increased to keep pace with the candidate.

    public static int[] generateFirstNPrimes(int n) {
        initializeTheGenerator(n);

        for (candidate = 5; primesFound < n; candidate += 2) {
            increaseEachPrimeMultipleToOrBeyondCandidate();
            if (candidateIsNotOneOfThePrimeMultiples()) {
                registerTheCandidateAsPrime();
            }
        }
        return primes;
    }

    private static void initializeTheGenerator(int n) {
        primes = new int[n];
        primeMultiples = new int[n];
        lastRelevantMultiple = 1;

        // prime the pump. (Sorry, couldn't resist.)
        primesFound = 2;
        primes[0] = 2;
        primes[1] = 3;

        primeMultiples[0] = -1;// irrelevant
        primeMultiples[1] = 9;
    }

    private static void increaseEachPrimeMultipleToOrBeyondCandidate() {
        if (candidate >= primeMultiples[lastRelevantMultiple])
            lastRelevantMultiple++;

        for (int i = 1; i <= lastRelevantMultiple; i++)
            while (primeMultiples[i] < candidate)
                primeMultiples[i] += 2 * primes[i];
    }

    private static boolean candidateIsNotOneOfThePrimeMultiples() {
        for (int i = 1; i <= lastRelevantMultiple; i++)
            if (primeMultiples[i] == candidate)
                return false;
        return true;
    }

    private static void registerTheCandidateAsPrime() {
        primes[primesFound] = candidate;
        primeMultiples[primesFound] = candidate * candidate;
        primesFound++;
    }
}
```

### John

This version is a considerable improvement over the version in _Clean Code_.
Reducing the number of methods made the code easier to read and resulted
in cleaner interfaces. If it were properly commented, I think this version
would be about as easy to read as my version (the additional methods you
created didn't particularly help, but they didn't hurt either). I suspect
that if we polled readers, some would like your version better and some
would prefer mine.

Unfortunately, this revision of the code creates a serious performance
regression: I measured a factor of 3-4x slowdown compared to either
of the earlier revisions. The problem is that you changed the processing of a
particular candidate from a single loop to two loops (the `increaseEach...` and
`candidateIsNot...` methods). In the loop from earlier revisions, and in
the `candidateIsNot`
method, the loop aborts once the candidate is disqualified (and
most candidates are quickly eliminated). However,
`increaseEach...` must examine every entry in `primeMultiples`.
This results in 5-10x as many loop iterations and a 3-4x overall slowdown.

Given that the whole reason for the current algorithm (and its complexity)
is to maximize performance, this slowdown is unacceptable. The two
methods must be combined.

I think what happened here is that you were so focused on something
that isn't actually all that important (creating the tiniest possible methods)
that you dropped the ball on other issues that really are important.
We have now seen this twice. In the original version of `PrimeGenerator`
you were so determined to make tiny methods that you didn't notice that the
code was becoming incomprehensible. In this version you were so eager to
chop up my single method that you didn't notice that you were blowing up the
performance.

I don't think this was just an unfortunate combination of oversights.
One of the most important things
in software design is to identify what is important and focus on that;
if you focus on things that are unimportant, you're likely to mess up the
things that are important.

The code in your revision is still under-commented. You believe
that there is no meaningful way for comments to assist the reader in
understanding the code. I think this stems from your general disbelief in
the value of comments; you are quick to throw in the towel.
This algorithm is unusually difficult to explain,
but I still believe that comments can help. For example, I believe you
must make some attempt to help readers understand why the first multiple
for a prime is the square of the prime. You have taken a lot of time to
develop your understanding of this; surely there must be some way to convey
that understanding to others? If you had included that information in
your original version of the code you could have saved yourself that long
bike ride.
Giving up on this is an abdication of professional responsibility.

The few comments that you included in your revision are of little value.
The first comment is too cryptic to provide much help: I can't
make any sense of the phrase "predicting the next composite number and
skipping over it" even though I completely understand the code it purports
to explain. One of the comments is just a joke; I was surprised to see
this, given your opposition to extraneous comments.

Clearly you and I live in different universes when it comes to comments.

Finally, I don't understand why you are offended by the labeled `continue`
statement in my code. This is a clean and elegant solution to the problem
of escaping from nested loops. I wish more languages
had this feature; the alternative is awkward code where you set a variable,
then exit one level of loop, then check the variable and exit the next
level.

### UB

Good catch! I would have caught that too had I thought to profile the solution. You are right that separating the two loops added some unecessary iteration. I found a nice way to solve that problem without using the horrible `continue`. My updated version is now faster than yours! A million primes in 440ms as opposed to yours which takes 561ms. ;-) Below are just the changes.

```java
public static int[] generateFirstNPrimes(int n) {
    initializeTheGenerator(n);

    for (candidate = 5; primesFound < n; candidate += 2)
        if (candidateIsPrime())
            registerTheCandidateAsPrime();

    return primes;
}

private static boolean candidateIsPrime() {
    if (candidate >= primeMultiples[lastRelevantMultiple])
        lastRelevantMultiple++;

    for (int i = 1; i <= lastRelevantMultiple; i++) {
        while (primeMultiples[i] < candidate)
            primeMultiples[i] += 2 * primes[i];
        if (primeMultiples[i] == candidate)
            return false;
    }
    return true;
}
```

### John

Yep, that fixes the problem. I note that you are now down to 4 methods,
from 8 in the _Clean Code_ version.
