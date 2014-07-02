====================
Introducing the EPFL
====================


The **E**\ PFL **P**\ ython **F**\ rontend **L**\ ogic is a framework for creating web applications.
EPFL is very specialized on **form based** web applications.

So it very suitable for something like this:

.. image:: _static/epfl_form.png
    :width: 50%
    :align: center

But not for this:

.. image:: _static/billigerde_screen.png
    :width: 50%
    :align: center


Because of it's design and the "server-side-state"-feature the number of concurrent sessions is directly related to it's memory usage. (Maybe 10k per session and 8h-24h session TTL) So again, an edit-frontend for company wide data is it's strength, a website accessible for everybody from the internet maybe not.


The epfl is a page/component oriented framework implemented as pyramid-extension. You compose single pages of reusable components. 

The key ideas are:

- batteries included! (a rich set of components and features you really need)
    - provide a set of reusable components -> speed up development
- fewer options, or: one way to do it right(tm)!
    - give flexibility - but only where needed
- few building blocks (pages and components)
- locality
    - aspects of the application should not be spread over multiple locations -> easy to understand and find functionality
- event driven programming model
- server side state (every user input is available anytime on the server)
- no javascript coding necessary

The EPFL uses the following projects:

- python
- pyramid
- WTForms
- jinja2
- ...

