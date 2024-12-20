+++
title = "35: The Golden Rule of API Design"
weight = 35
+++

API design is tough, particularly in the large. If you are designing an API that is going to have hundreds or thousands of users, you have to think about how you might change it in the future and whether your changes might break client code. Beyond that, you have to think about how users of your API affect you. If one of your API classes uses one of its own methods internally, you have to remember that a user could subclass your class and override it, and that could be disastrous. You wouldn't be able to change that method because some of your users have given it a different meaning. Your future internal implementation choices are at the mercy of your users.

API developers solve this problem in various ways, but the easiest way is to lock down the API. If you are working in Java you might be tempted to make most of your classes and methods final. In C#, you might make your classes and methods sealed. Regardless of the language you are using, you might be tempted to present your API through a singleton or use static factory methods so that you can guard it from people who might override behavior and use your code in ways which may constrain your choices later. This all seems reasonable, but is it really?

Over the past decade, we've gradually realized that unit testing is an extremely important part of practice, but that lesson has not completely permeated the industry. The evidence is all around us. Take an arbitrary untested class that uses a third-party API and try to write unit tests for it. Most of the time, you'll run into trouble. You'll find that the code using the API is stuck to it like glue. There's no way to impersonate the API classes so that you can sense your code's interactions with them, or supply return values for testing.

Over time, this will get better, but only if we start to see testing as a real use case when we design APIs. Unfortunately, it's a little bit more involved than just testing our code. That's where the **Golden Rule of API Design** fits in: *It's not enough to write tests for an API you develop; you have to write unit tests for code that uses your API. When you do, you learn first-hand the hurdles that your users will have to overcome when they try to test their code independently.*

There is no one way to make it easy for developers to test code which uses your API. `static`, `final`, and `sealed` are not inherently bad constructs. They can be useful at times. But it is important to be aware of the testing issue and, to do that, you have to experience it yourself. Once you have, you can approach it as you would any other design challenge.

By [Michael Feathers](http://programmer.97things.oreilly.com/wiki/index.php/Michael_Feathers)