Layouting Pages
===============


Common pitfalls:
----------------

- Do not use a component multiple times in one page.
This also means that you can not split a form into multiple parts (e.g. opening and closing the form component multiple times).
If you need to split a form in multiple parts across the page you must:
    - open and close the form at the outer most part of the page (but then a redraw redraws the complete thing)
    - split the form in to multiple components (and handle them separatly)


