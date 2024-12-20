+++
title = "80: Test for Required Behavior, not Incidental Behavior"
weight = 80
+++

A common pitfall in testing is to assume that exactly what an implementation does is precisely what you want to test for. At first glance this sounds more like a virtue than a pitfall. Phrased another way, however, the issue becomes more obvious: A common pitfall in testing is to hardwire tests to the specifics of an implementation, where those specifics are incidental and have no bearing on the desired functionality.

When tests are hardwired to implementation incidentals, changes to the implementation that are actually compatible with the required behavior may cause tests to fail, leading to false positives. Programmers typically respond either by rewriting the test or by rewriting the code. Assuming that a false positive is actually a true positive is often a consequence of fear, uncertainty, or doubt. It has the effect of raising the status of incidental behavior to required behavior. In rewriting a test, programmers either refocus the test on the required behavior (good) or simply hardwire it to the new implementation (not good). Tests need to be sufficiently precise, but they also need to be accurate.

For example, in a three-way comparison, such as C's `strcmp` or Java's `String.compareTo`, the requirements on the result are that it is negative if the left-hand side is less than the right, positive if the left-hand side is greater than the right, and zero if they are considered equal. This style of comparison is used in many APIs, including the comparator for C's `qsort` function and `compareTo` in Java's `Comparable` interface. Although the specific values `-1` and `+1` are commonly used in implementations to signify *less than* and *greater than*, respectively, programmers often mistakenly assume that these values represent the actual requirement and consequently write tests that nail this assumption up in public.

A similar issue arises with tests that assert spacing, precise wording, and other aspects of textual formatting and presentation that are incidental. Unless you are writing, for example, an XML generator that offers configurable formatting, spacing should not be significant to the outcome. Likewise, hardwiring placement of buttons and labels on UI controls reduces the option to change and refine these incidentals in future. Minor changes in implementation and inconsequential changes in formatting suddenly become build breakers.

Overspecified tests are often a problem with whitebox approaches to unit testing. Whitebox tests use the structure of the code to determine the test cases needed. The typical failure mode of whitebox testing is that the tests end up asserting that the code does what the code does. Simply restating what is already obvious from the code adds no value and leads to a false sense of progress and security.

To be effective, tests need to state contractual obligations rather than parrot implementations. They need to take a blackbox view of the units under test, sketching out the interface contracts in executable form. Therefore, align tested behavior with required behavior.

By [Kevlin Henney](http://programmer.97things.oreilly.com/wiki/index.php/Kevlin_Henney)