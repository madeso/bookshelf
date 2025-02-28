+++
title = "13: Code Layout Matters"
weight = 13
+++

An infeasible number of years ago I worked on a Cobol system where staff weren't allowed to change the indentation unless they already had a reason to change the code, because someone once broke something by letting a line slip into one of the special columns at the beginning of a line. This applied even if the layout was misleading, which it sometimes was, so we had to read the code very carefully because we couldn't trust it. The policy must have cost a fortune in programmer drag.

There's research to show that we all spend much more of our programming time navigating and reading code — finding *where* to make the change — than actually typing, so that's what we want to optimize for.

- *Easy to scan.* People are really good at visual pattern matching (a leftover from the time when we had to spot lions on the savannah), so I can help myself by making everything that isn't directly relevant to the domain, all the "accidental complexity" that comes with most commercial languages, fade into the background by standardizing it. If code that behaves the same looks the same, then my perceptual system will help me pick out the differences. That's why I also observe conventions about how to lay out the parts of a class within a compilation unit: constants, fields, public methods, private methods.

- *Expressive layout.* We've all learned to take the time to find the right names so that our code expresses as clearly as possible what it does, rather than just listing the steps — right? The code's layout is part of this expressiveness too. A first cut is to have the team agree on an automatic formatter for the basics, then I might make adjustments by hand while I'm coding. Unless there's active dissension, a team will quickly converge on a common "hand-finished" style. A formatter cannot understand my intentions (I should know, I once wrote one), and it's more important to me that the line breaks and groupings reflect the intention of the code, not just the syntax of the language. (Kevin McGuire freed me from my bondage to automatic code formatters.)

- *Compact format.* The more I can get on a screen, the more I can see without breaking context by scrolling or switching files, which means I can keep less state in my head. Long procedure comments and lots of whitespace made sense for 8-character names and line printers, but now I live in an IDE that does syntax coloring and cross linking. Pixels are my limiting factor so I want every one to contribute towards my understanding of the code. I want the layout to help me understand the code, but no more than that.

A non-programmer friend once remarked that code looks like poetry. I get that feeling from really good code, that everything in the text has a purpose and that it's there to help me understand the idea. Unfortunately, writing code doesn't have the same romantic image as writing poetry.

By [Steve Freeman](http://programmer.97things.oreilly.com/wiki/index.php/Steve_Freeman)
