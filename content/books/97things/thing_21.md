+++
title = "21: Distinguish Business Exceptions from Technical"
weight = 21
+++

There are basically two reasons that things go wrong at runtime: technical problems that prevent us from using the application and business logic that prevents us from misusing the application. Most modern languages, such as LISP, Java, Smalltalk, and C#, use exceptions to signal both these situations. However, the two situations are so different that they should be carefully held apart. It is a potential source of confusion to represent them both using the same exception hierarchy, not to mention the same exception class.

An unresolvable technical problem can occur when there is a programming error. For example, if you try to access element 83 from an array of size 17, then the program is clearly off track, and some exception should result. The subtler version is calling some library code with inappropriate arguments, causing the same situation on the inside of the library.

It would be a mistake to attempt to resolve these situations you caused yourself. Instead we let the exception bubble up to the highest architectural level and let some general exception-handling mechanism do what it can to ensure the system is in a safe state, such as rolling back a transaction, logging and alerting administration, and reporting back (politely) to the user.

A variant of this situation is when you are in the "library situation" and a caller has broken the contract of your method, e.g., passing a totally bizarre argument or not having a dependent object set up properly. This is on a par with accessing 83rd element from 17: the caller should have checked; not doing so is a programmer error on the client side. The proper response is to throw a technical exception.

A different, but still technical, situation is when the program cannot proceed because of a problem in the execution environment, such as an unresponsive database. In this situation you must assume that the infrastructure did what it could to resolve the situation — repairing connections and retrying a reasonable number of times — and failed. Even if the cause is different, the situation for the calling code is similar: there is little it can do about it. So, we signal the situation through an exception that we let bubble up to the general exception handling mechanism.

In contrast to these, we have the situation where you cannot complete the call for a domain-logical reason. In this case we have encountered a situation that is an exception, i.e., unusual and undesirable, but not bizarre or programmatically in error. For example, if I try to withdraw money from an account with insufficient funds. In other words, this kind of situation is a part of the contract, and throwing an exception is just an *alternative return path* that is part of the model and that the client should be aware of and be prepared to handle. For these situations it is appropriate to create a specific exception or a separate exception hierarchy so that the client can handle the situation on its own terms.

Mixing technical exceptions and business exceptions in the same hierarchy blurs the distinction and confuses the caller about what the method contract is, what conditions it is required to ensure before calling, and what situations it is supposed to handle. Separating the cases gives clarity and increases the chances that technical exceptions will be handled by some application framework, while the business domain exceptions actually are considered and handled by the client code.

By [Dan Bergh Johnsson](http://programmer.97things.oreilly.com/wiki/index.php/Dan_Bergh_Johnsson)