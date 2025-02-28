+++
title = "42: Keep the Build Clean"
weight = 42
+++

Have you ever looked at a list of compiler warnings the length of an essay on bad coding and thought to yourself: "You know, I really should do something about that... but I don't have time just now?" On the other hand, have you ever looked at a lone warning that just appeared in a compilation and just fixed it?

When I start a new project from scratch, there are no warnings, no clutter, no problems. But as the code base grows, if I don't pay attention, the clutter, the cruft, the warnings, and the problems can start piling up. When there's a lot of noise, it's much harder to find the warning that I really want to read among the hundreds of warnings I don't care about.

To make warnings useful again, I try to use a zero-tolerance policy for warnings from the build. Even if the warning isn't important, I deal with it. If not critical, but still relevant, I fix it. If the compiler warns about a potential null-pointer exception, I fix the cause — even if I "know" the problem will never show up in production. If the embedded documentation (Javadoc or similar) refers to parameters that have been removed or renamed, I clean up the documentation.

If it's something I really don't care about and that really doesn't matter, I ask the team if we can change our warning policy. For example, I find that documenting the parameters and return value of a method in many cases doesn't add any value, so it shouldn't be a warning if they are missing. Or, upgrading to a new version of the programming language may make code that was previously OK now emit warnings. For example, when Java 5 introduced generics, all the old code that didn't specify the generic type parameter would give a warning. This is a sort of warning I don't want to be nagged about (at least, not yet). Having a set of warnings that are out of step with reality does not serve anyone.

By making sure that the build is always clean, I will not have to decide that a warning is irrelevant every time I encounter it. Ignoring things is mental work, and I need to get rid of all the unnecessary mental work I can. Having a clean build also makes it easier for someone else to take over my work. If I leave the warnings, someone else will have to wade through what is relevant and what is not. Or more likely, just ignore all the warnings, including the significant ones.

Warnings from your build are useful. You just need to get rid of the noise to start noticing them. Don't wait for a big clean-up. When something appears that you don't want to see, deal with it right away. Either fix the source of the warning, suppress this warning or fix the warning policies of your tool. Keeping the build clean is not just about keeping it free of compilation errors or test failures: Warnings are also an important and critical part of code hygiene.

By [Johannes Brodwall](http://programmer.97things.oreilly.com/wiki/index.php/Johannes_Brodwall)