+++
title = "14: Code Reviews"
weight = 14
+++

You should do code reviews. Why? Because they *increase code quality* and *reduce defect rate*. But not necessarily for the reasons you might think.

Because they may previously have had some bad experiences with reviews, many programmers tend to dislike code reviews. I have seen organizations that require that all code pass a formal review before being deployed to production. Often it is the architect or a lead developer doing this review, a practice that can be described as *architect reviews everything*. This is stated in their software development process manual, so therefore the programmers must comply. There may be some organizations that need such a rigid and formal process, but most do not. In most organizations such an approach is counterproductive. Reviewees can feel like they are being judged by a parole board. Reviewers need both the time to read the code and the time to keep up to date with all the details of the system. The reviewers can rapidly become the bottleneck in this process, and the process soon degenerates.

Instead of simply correcting mistakes in code, the purpose of code reviews should be to *share knowledge* and establish common coding guidelines. Sharing your code with other programmers enables collective code ownership. Let a random team member *walk through the code* with the rest of the team. Instead of looking for errors you should review the code by trying to learn it and understand it.

Be gentle during code reviews. Ensure that comments are *constructive, not caustic*. Introduce different *review roles* for the review meeting, to avoid having organizational seniority among team members affect the code review. Examples of roles could include having one reviewer focus on documentation, another on exceptions, and a third to look at the functionality. This approach helps to spread the review burden across the team members.

Have a regular *code review* day each week. Spend a couple of hours in a review meeting. Rotate the reviewee every meeting in a simple round-robin pattern. Remember to switch roles among team members every review meeting too. *Involve newbies* in code reviews. They may be inexperienced, but their fresh university knowledge can provide a different perspective. *Involve experts* for their experience and knowledge. They will identify error-prone code faster and with more accuracy. Code reviews will flow more easily if the team has *coding conventions* that are checked by tools. That way, code formatting will never be discussed during the code review meeting.

*Making code reviews fun* is perhaps the most important contributor to success. Reviews are about the people reviewing. If the review meeting is painful or dull it will be hard to motivate anyone. Make it an *informal code review* whose prime purpose is sharing knowledge between team members. Leave sarcastic comments outside and bring a cake or brown bag lunch instead.

by [Mattias Karlsson](http://programmer.97things.oreilly.com/wiki/index.php/Mattias_Karlsson)