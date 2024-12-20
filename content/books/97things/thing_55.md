+++
title = "55: Make Interfaces Easy to Use Correctly and Hard to Use Incorrectly"
weight = 55
+++

One of the most common tasks in software development is interface specification. Interfaces occur at the highest level of abstraction (user interfaces), at the lowest (function interfaces), and at levels in between (class interfaces, library interfaces, etc.). Regardless of whether you work with end users to specify how they'll interact with a system, collaborate with developers to specify an API, or declare functions private to a class, interface design is an important part of your job. If you do it well, your interfaces will be a pleasure to use and will boost others' productivity. If you do it poorly, your interfaces will be a source of frustration and errors.

Good interfaces are:

- **Easy to use correctly.** People using a well-designed interface almost always use the interface correctly, because that's the path of least resistance. In a GUI, they almost always click on the right icon, button, or menu entry, because it's the obvious and easy thing to do. In an API, they almost always pass the correct parameters with the correct values, because that's what's most natural. With interfaces that are easy to use correctly, *things just work.*
- **Hard to use incorrectly.** Good interfaces anticipate mistakes people might make and make them difficult — ideally impossible — to commit. A GUI might disable or remove commands that make no sense in the current context, for example, or an API might eliminate argument-ordering problems by allowing parameters to be passed in any order.

A good way to design interfaces that are easy to use correctly is to exercise them before they exist. Mock up a GUI — possibly on a whiteboard or using index cards on a table — and play with it before any underlying code has been created. Write calls to an API before the functions have been declared. Walk through common use cases and specify how you *want* the interface to behave. What do you *want* to be able to click on? What do you *want* to be able to pass? Easy to use interfaces seem natural, because they let you do what you want to do. You're more likely to come up with such interfaces if you develop them from a user's point of view. (This perspective is one of the strengths of test-first programming.)

Making interfaces hard to use incorrectly requires two things. First, you must anticipate errors users might make and find ways to prevent them. Second, you must observe how an interface is misused during early release and modify the interface — yes, modify the interface! — to prevent such errors. The best way to prevent incorrect use is to make such use impossible. If users keep wanting to undo an irrevocable action, try to make the action revocable. If they keep passing the wrong value to an API, do your best to modify the API to take the values that users want to pass.

Above all, remember that interfaces exist for the convenience of their users, not their implementers.

By [Scott Meyers](http://programmer.97things.oreilly.com/wiki/index.php/Scott_Meyers)