+++
title = "John's Rewrite of PrimeGenerator"
weight = 40
+++

### John

I mentioned that I ask the students in my software design class to rewrite
`PrimeGenerator` to fix all of its design problems. Here is my rewrite
(note: this was written before we began our discussion; given what I
have learned during the discussion, I would now change several of the
comments, but I have left this in its original form):

```java
package literatePrimes;

import java.util.ArrayList;

public class PrimeGenerator2 {

    /**
     * Computes the first prime numbers; the return value contains the
     * computed primes, in increasing order of size.
     * @param n
     *      How many prime numbers to compute.
     */
    public static int[] generate(int n) {
        int[] primes = new int[n];

        // Used to test efficiently (without division) whether a candidate
        // is a multiple of a previously-encountered prime number. Each entry
        // here contains an odd multiple of the corresponding entry in
        // primes. Entries increase monotonically.
        int[] multiples = new int[n];

        // Index of the last value in multiples that we need to consider
        // when testing candidates (all elements after this are greater
        // than our current candidate, so they don't need to be considered).
        int lastMultiple = 0;

        // Number of valid entries in primes.
        int primesFound = 1;

        primes[0] = 2;
        multiples[0] = 4;

        // Each iteration through this loop considers one candidate; skip
        // the even numbers, since they can't be prime.
        candidates: for (int candidate = 3; primesFound < n; candidate += 2) {
            if (candidate >= multiples[lastMultiple]) {
                lastMultiple++;
            }

            // Each iteration of this loop tests the candidate against one
            // potential prime factor. Skip the first factor (2) since we
            // only consider odd candidates.
            for (int i = 1; i <= lastMultiple; i++) {
                while (multiples[i] < candidate) {
                    multiples[i] += 2*primes[i];
                }
                if (multiples[i] == candidate) {
                    continue candidates;
                }
            }
            primes[primesFound] = candidate;

            // Start with the prime's square here, rather than 3x the prime.
            // This saves time and is safe because all of the intervening
            // multiples will be detected by smaller prime numbers. As an
            // example, consider the prime 7: the value in multiples will
            // start at 49; 21 will be ruled out as a multiple of 3, and
            // 35 will be ruled out as a multiple of 5, so 49 is the first
            // multiple that won't be ruled out by a smaller prime.
            multiples[primesFound] = candidate*candidate;
            primesFound++;
        }
        return primes;
    }
}
```

Everyone can read this and decide for themselves whether they think
it is easier to understand than the original. I'd like to mention a
couple of overall things:

-   There is only one method. I didn't subdivide it because I felt the method already divides naturally into pieces that are distinct and understandable. It didn't seem to me that pulling out methods would improve readability significantly. When students rewrite the code, they typically have 2 or 3 methods, and those are usually OK too.
-   There are a _lot_ of comments. It's extremely rare for me to write code with this density of comments. Most methods I write have no comments in the body, just a header comment describing the interface. But this code is subtle and tricky, so it needs a lot of comments to make the subtleties clear to readers. The long length of some of the comments is a red flag indicating that I struggled to find a clear and simple explanation for the code. Even with all the additional explanatory material this version is a bit shorter than the original (65 lines vs. 70).

### UB

I presume this is a complete rewrite. My guess is that you worked to understand the algorithm from _Clean Code_ and then wrote this from scratch. If that's so, then fair enough.

In _Clean Code_ I _refactored_ Knuth's algorithm in order to give it a little structure. That's not the same as a complete rewrite.

Having said that, your version is much better than either Knuth's or mine.

I wrote that chapter 18 years ago, so it's been a long time since I saw and understood this algorithm. When I first saw your challenge I thought: "Oh, I can figure out my own code!" But, no. I could see all the moving parts, but I could not figure out why those moving parts generated a list of prime numbers.

So then I looked at your code. I had the same problem. I could see all the moving parts, all with comments, but I still could not figure out why those moving parts generated a list of prime numbers.

Figuring that out required a lot of staring at the ceiling, closing my eyes, visualizing, and riding my bike.

Among the problems I had were the comments you wrote. Let's take them one at a time.

```java
/**
 * Computes the first prime numbers; the return value contains the
 * computed primes, in increasing order of size.
 * @param n
 *      How many prime numbers to compute.
 */
public static int[] generate(int n) {
```

It seems to me that this would be better as:

```java
public static int[] generateNPrimeNumbers(int n) {
```

or if you must:

```java
//Return the first n prime numbers
public static int[] generate(int n) {
```

I'm not opposed to Javadocs as a rule; but I write them only when absolutely necessary. I also have an aversion for descriptions and `@param` statements that are perfectly obvious from the method signature.

The next comment cost me a good 20 minutes of puzzling things out.

```java
// Used to test efficiently (without division) whether a candidate
// is a multiple of a previously-encountered prime number. Each entry
// here contains an odd multiple of the corresponding entry in
// primes. Entries increase monotonically.
```

First of all I'm not sure why the "division" statement is necessary. I'm old school so I expect that everyone knows to avoid division in inner loops if it can be avoided. But maybe I'm wrong about that...

Also, the _Sieve of Eratosthenes_ does not do division, and is a lot easier to understand _and explain_ than this algorithm. So why this particular algorithm? I think Knuth was trying to save _memory_ -- and in 1982 saving memory was important. This algorithm uses a lot less memory than the sieve.

Then came the phrase: `Each entry here contains an odd multiple...`. I looked at that, and then at the code, and I saw: `multiples[0] = 4;`.

"That's not odd" I said to myself. "So maybe he meant even."

So then I looked down and saw: `multiples[i] += 2*primes[i];`

"That's adding an even number!" I said to myself. "I'm pretty sure he meant to say 'even' instead of 'odd'."

I hadn't yet worked out what the `multiples` array was. So I thought it was perfectly reasonable that it would have even numbers in it, and that your comment was simply an understandable word transposition. After all, there's no compiler for comments so they suffer from the kinds of mistakes that humans often make with words.

It was only when I got to `multiples[primesFound] = candidate*candidate;` that I started to question things. If the `candidate` is prime, shouldn't `prime*prime` be odd in every case beyond 2? I had to do the math in my head to prove that. (2n+1)(2n+1) = 4n^2+4n+1 ... Yeah, that's odd.

OK, so the `multiples` array is full of odd multiples, except for the first element, since it will be muliples of 2.

So perhaps that comment should be:

```java
// multiples of corresponding prime.
```

Or perhaps we should change the name of the array to something like `primeMultiples` and drop the comment altogether.

Moving on to the next comment:

```java
// Each iteration of this loop tests the candidate against one
// potential prime factor. Skip the first factor (2) since we
// only consider odd candidates.
```

That doesn't make a lot of sense. The code it's talking about is:

```java
for (int i = 1; i <= lastMultiple; i++) {
    while (multiples[i] < candidate) {
```

The `multiples` array, as we have now learned, is an array of _multiples_ of prime numbers. This loop is not testing the candidate against prime _factors_, it's testing it against the current prime _multiples_.

Fortunately for me the third of fourth time I read this comment I realized that you really meant to use the word "multiples". But the only way for me to know that was to understand the algorithm. And when I understand the algorithm, why do I need the comment?

That left me with one final question. What the deuce was the reason behind:

```java
multiples[primesFound] = candidate*candidate;
```

Why the square? That makes no sense. So I changed it to:

```java
multiples[primesFound] = candidate;
```

And it worked just fine. So this must be an optimization of some kind.

Your comment to explain this is:

```java
// Start with the prime's square here, rather than 3x the prime.
// This saves time and is safe because all of the intervening
// multiples will be detected by smaller prime numbers. As an
// example, consider the prime 7: the value in multiples will
// start at 49; 21 will be ruled out as a multiple of 3, and
// 35 will be ruled out as a multiple of 5, so 49 is the first
// multiple that won't be ruled out by a smaller prime.
```

The first few times I read this it made no sense to me at all. It was just a jumble of numbers.

I stared at the ceiling, and closed my eyes to visualize. I couldn't see it. So I went on a long contemplative bike ride during which I realized that the prime multiples of 2 will at one point contain 2\*3 and then 2\*5. So the `multiples` array will at some point contain multiples of primes _larger_ than the prime they represent. _And it clicked!_

Suddenly it all made sense. I realized that the `multiples` array was the equivalent of the array of booleans we use in the _Sieve of Eratosthenes_ -- but with a really interesting twist. If you were to do the sieve on a whiteboard, you _could_ erase every number less than the candidate, and only cross out the numbers that were the next multiples of all the previous primes.

That explanation makes perfect sense to me -- now, but I'd be willing to bet that those who are reading it are puzzling over it. The idea is just hard to explain.

Finally I went back to your comment and could see what you were saying.

## A Tale of Two Programmers

The bottom line here is that you and I both fell into the same trap. I refactored that old algorithm 18 years ago, and I thought all those method and variable names would make my intent clear -- _because I understood that algorithm_.

You wrote that code awhile back and decorated it with comments that you thought would explain your intent -- _because you understood that algorithm_.

But my names didn't help me 18 years later. They didn't help you, or your students either. And your comments didn't help me.

We were inside the box trying to communicate to those who stood outside and could not see what we saw.

The bottom line is that it is very difficult to explain something to someone who is not intimate with the details you are trying to explain. Often our explanations make sense only after the reader has worked out the details for themself.

### John

There's a lot of stuff in your discussion above, but I think it all boils down
to one thing: you don't like the comments that I wrote. As I mentioned earlier,
complexity is in the eye of the reader: if you say that my comments were
confusing or didn't help you to understand the code, then I have to take that
seriously.

At the same time, you have made it clear that you don't see much value in
comments in general. Your preference is to have essentially no
comments for this code (or any code). You argue above that there is simply nothing that
comments can do to make the code easier to understand; the only way to
understand the code is to read the code. That is a cop-out.

### UB

Sorry to interrupt you; but I think you are overstating my position. I certainly never said that comments can never be helpful. Sometimes, of course, they are. What I said was that I only trust them if the code validates them. Sometimes a comment will make that validation a lot easier.

### John

You keep saying that you sometimes find use for comments, but the reality
is that "sometimes" almost never occurs in your code. We'll see this when
we look at your revision of my code.

Now back to my point. In order to
write our various versions of the code, you and I had to accumulate a lot of
knowledge about the algorithm, such as why it's OK for the first multiple
of a prime to be its square. Unfortunately, not all of that knowledge can
be represented in the code. It is our professional responsibility to do
the best we can to convey
that knowledge in comments, so that readers do not
have to reconstruct it over and over. Even if the resulting comments are
imperfect, they will make the code easier to understand.

If a situation like this occurred in real life I would work with
you and others to improve my comments. For example, I would ask you
questions to get a better sense of
why the "squared prime" comment didn't seem to help you:

-   Are there things in the comment that are misleading or confusing?
-   Is there some important piece of information you acquired on your
    bike ride that suddenly made things clear?

I would also show the comment to a few other people to get their takes
on it. Then I would rework the comment to improve it.

Given your fundamental disbelief in comments, I think it's likely that
you would still see no value in the comment, even after my reworking.
In this case I would show the comment to other people, particularly those
who have a more positive view of comments in general, and get
their input. As long as the comment is not misleading and at least a few
people found it helpful, I would retain it.

Now let me discuss two few specific comments that you objected to. The
first comment was the one for the `multiples` variable:

```java
// Used to test efficiently (without division) whether a candidate
// is a multiple of a previously-encountered prime number. Each entry
// here contains an odd multiple of the corresponding entry in
// primes. Entries increase monotonically.
```

There is a bug in this comment that you exposed (the first entry is not odd);
good catch! You then argued that most of the information in the comment
is unnecessary and proposed this as an alternative:

```java
// multiples of corresponding prime.
```

You have left out too much useful information here. For example, I don't think
it is safe to assume that readers will figure out that the motivation is
avoiding divisions. It's always better to state these assumptions and
motivations clearly so that there will be no confusion. And I think it's
helpful for readers to know that these entries never decrease.
I would simply fix the bug, leaving all of the information intact:

```java
// Used to test efficiently (without division) whether a candidate
// is a multiple of a previously-encountered prime number. Each entry
// (except the first, which is never used) contains an odd multiple of
// the corresponding entry in primes. Entries increase monotonically.
```

The second comment was this one, for the `for` loop:

```java
// Each iteration of this loop tests the candidate against one
// potential prime factor. Skip the first factor (2) since we
// only consider odd candidates.
```

You objected to this comment because the code of the loop doesn't actually
test the candidate against the prime factor; it tests it against a multiple.
When I write implementation comments like this, my goal is not to restate
the code; comments like that don't usually provide much value. The goal here was
to say _what_ the code is doing in a logical sense, not _how_ it does it.
In that sense, the comment is correct.

However, if a comment causes confusion in the reader, then it is not a
good comment. Thus I would rewrite this comment to make it clear that
it describes the abstract function of the code, not its
precise behavior:

```java
// Each iteration of this loop considers one existing prime, ruling
// out the candidate if it is a multiple of that prime. Skip the
// first prime (2) since we only consider odd candidates.
```

To conclude, I agree with your assertion "it is very difficult to explain
something to someone who is not intimate with the details you are trying
to explain." And yet, it is our responsibility as programmers to do exactly
that.

### UB

I'm glad we agree. We also agree about getting others to review the code and make recommendations on the code _and_ the comments.
