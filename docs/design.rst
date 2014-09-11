EPFL design decisions
=====================

Server side state
-----------------

What is the main idea behind server side state?

In webapplications there are many ways to transport data from the client to the server and back. You can submit forms, use ajax-requests, replace data in templates, use JSON, not use JSON, ... Additionally if you want to persist data for a certain live time (e.g. the timespan you edit a object with a form), you could save the data in the session, use hidden form fields, manipulate URLs on client and/or server side, use cookies. It gets worse if you combine some of these possibilities. You often find this mixture in real life projects, because all of these technologies have thier down- and up-sides and often the way data is transported and logical transactions are handeled is not very well focussed and regulated in today's frameworks.

The issue arrises when unexpected effects occur because of misunderstood ways the client and the server handle thier state. Suddenly a client-side state manipulation is interfering with server side persistance of the same variable.

Server side state adresses this issue:

1. The way all state is transfered between client and server is standardized and only done by the framework
2. There is only one place where state is persisted: at the server
3. There is only one place where state is manipulated by the application: the server
4. There is only one language state manipulation is done (by the application): python

Because it is easy and convenient for the developer to have all state at server side automatically available there is no need to spread the business logic all over the place.


