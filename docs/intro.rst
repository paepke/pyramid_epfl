================
Introducing EPFL
================

---------
Why EPFL?
---------

**E**\ PFL **P**\ ython **F**\ rontend **L**\ ogic is a framework for creating form based web applications. Its purpose
is to create easy to use business application frontends.


.. |epflform| image:: _static/epfl_form.png
    :width: 100%

.. |eftext| replace:: So it's very suitable for something like this, ...

.. |bdeimg| image:: _static/billigerde_screen.png
    :width: 100%

.. |bdetext| replace:: ... and definitely not suitable for anything like this.

+------------+-----------+
| |eftext|   | |bdetext| |
| |epflform| | |bdeimg|  |
+------------+-----------+


Due to its design and the "server-side-state"-feature EPFL is somewhat memory intensive. The number of concurrent
sessions is directly related to its memory usage. Therefore keep in mind: EPFLs purpose is to serve as an edit-frontend
for company wide data, not as a website for the general public.

All of todays fancy frameworks are primarily general purpose tools supporting:
 - MVC Development
 - Responsive design
 - Interactivity

While all of these are important, none addresses the need for simple tools in case of repetitive development tasks.

EPFL fills that gap with:
 - Freedom of boilerplate*
 - Component driven development
 - Compatibility with any data source

\* almost, but who reads qualifiers anyways?

EPFL allows developers to focus on their logical workflows instead of the tassels on the handlebar. If the usecase
exists in your internal workflows then there's an EPFL Component for it. If there is no EPFL Component for it it's easy
to build one once and then reuse it everywhere.

EPFL has the flexibility you need without forcing you to jump through all the hoops other frameworks force you through.

-------------
What is EPFL?
-------------

EPFL provides you a server-side-only programming experience and structures your application-UI into pages and
components. Components can interact - even across pages. It provides a number of base components like table, tree, form
that you can customize and use in your application.

EPFL is written as pyramid extension and released under the repoze (http://repoze.org/license.html) license.

EPFL comes with:

- KISS:
    Offer one way to do it right but give flexibility as needed.
- Batteries included:
    It offers you a rich set of features you really need and provides you with reusable components to speed up
    development.
- Location:
    One Page per activity, one component per task, you see what you get and you find what you need.
- No jumping through hoops:
    If you really need to write Javascript, HTML or CSS you can, but you really don't need to.
- Event Driven Programming
- Server Side State


---------------
The EPFL design
---------------

.. toctree::
   :maxdepth: 2

   design