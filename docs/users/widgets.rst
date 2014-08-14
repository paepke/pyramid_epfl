Widgets
=======

To use a Widget the epfl class has to be imported first.

    .. code:: bash

        from solute import epfl

For every widget there can be set the parameters as shown below. Further each widget has its own specific parameters as shown below in the widgets section:

    .. code:: bash

        label=text              #The label of the button widget is the button text
        type=type               #input type e.g. type=int
        mandatory=bool
        description=text        #tooltip
        validators=validators

To get the values of a widget it cen be seted up as follows:

    .. code:: bash

            shipping_cost = epfl.fields.Entry(u"ShippingCosts",
                                              validators=[CurrencyValidation()])

The html/jinja part of the widget can be setup with:

    .. code-block :: html

        {{ form.button_widget }}                <!--the widget itself-->
        {{ form.button_widget.label }}          <!--the label of the widget-->
        {{ form.button_widget.validator_visual }}  <!--sets a * if the widget is mandatory-->
        <td class="epfl-form-field-error">{{ form.button_widget.errors | join(' ') }}</td>     <!--Error message (of the validators as well)-->
        {{ form.button_widget.tooltip() }}      <!--Shows the description text within a tootltip symbol-->

Basic
-----

The class basic contains numerous basic widgtes such as :py:func:`ButtonWidget` and an entry field in the following section the widgets and their parameters are explained.

    .. py:function:: EntryWidget()

        The EntryWidget makes it possible to enter text and numbers. It provides also a char count with a defined limitation as well as on change and on return functions. To use a char count the type with the ammount of chars have to be given and the ``char_count`` parameter has to be set to ``True``.

        .. code:: bash

            epfl.fields.Entry(type="char(250)",
                              char_count=Bool,
                              on_change=epflwidgetbase.EventType,
                              on_return=epflwidgetbase.EventType,
                              )

    .. py:function:: TextAreaWidget()

        The TextAreaWidget provides a field to show or entry text.

        .. code:: bash

            epfl.fields.TextArea(on_change=epflwidgetbase.EventType)


    .. py:function:: ButtonWidget()

        .. code:: bash

            eplf.fields.Button("on_click"="self.click")

        The fuction has to be written as a handle_ fuction e.g.

        .. code:: bash

            def handle_click(self):
                print "click"

    .. py:function:: RadioButtonWidget()

        .. code:: bash

            epfl.fields.RadioButton(choices="self.get_choices",
                                    on_change= epflwidgetbase.EventType)

        To use the radio button, the values have to be inserted in the ``choices`` parameter as a touple with id and value in a list. Further an ``on_change`` function can be used to trigger events by changing the marked button.

        .. code:: bash

            def get_choices():
                return[(1, u"New"),(2, u"Used"), (3, "b-stock")]

    .. py:function:: ButtonSetWidget()

        .. code:: bash

            epfl.fields.ButtonSet(choices="self.get_choices",
                                  on_change=epflwidgetbase.EventType)

        Similar to the RadioButtonWidget it provides a possibility to select different values. It acts like a radio button, but with
        a design of buttons. Here no 'real' buttons are provide, but a radio button widgte with another design.

        .. code:: bash

            def get_choices():
                return[(1, u"New"),(2, u"Used"), (3, "b-stock")]

    .. py:function:: Checkbox()

        The default value of a checkbox is ``False``.

        .. code:: bash

            epfl.fields.Checkbox(type=Bool)


CKEditor
--------

The CKEditor is a HTML text editor with various functions. It is fully open source and offers numerous option to customize it. The ``opts``
parameter contians all configuration parameter to customize the editor.

    .. py:function:: CKEditorWidget()

        .. code:: bash

            epfl.fields.CKEditor(opts={"insert_images": True,         #Enables/Disables image-handling
                                       "insert_link": True,           #Enables/Disables link-handling
                                       "show_elements_path": False,   #Enables/Disables the status-line with the html-elements-path from the current "cursor position"
                                       "cut_and_paste": True,
                                       "spellcheck": True,
                                       "insert_tables": True,
                                       "insert_hr": True,
                                       "insert_special": True,
                                       "show_source": True,
                                       "style": True,
                                       "format": True,
                                       "maximize": True,
                                       "wordcount": False,
                                       "paragraph": True,
                                       "charcount": False,
                                       "single_row_toolbar"=True})

    The height and width of the editor can be passed as kwarg-call-parameter in the jinja-template.
    Further there are some example options that can be used as opts parameter:

        .. code:: bash

            OPTS_MINIMAL_FORMATTING1 = {"insert_tables": False,
                                        "insert_images": False,
                                        "insert_links": False,
                                        "insert_hr": False,
                                        "insert_special": False,
                                        "show_source": False,
                                        "maximize": False,
                                        "style": False,
                                        "format": False,
                                        "paragraph": False,
                                        "single_row_toolbar": True,
                                        }

            OPTS_MINIMAL_FORMATTING2 = {"insert_tables": False,
                                        "insert_images": False,
                                        "insert_links": False,
                                        "insert_hr": False,
                                        "insert_special": False,
                                        "show_source": False,
                                        "maximize": False,
                                        "style": False,
                                        "format": False,
                                        "paragraph": True,
                                        "single_row_toolbar": True,
                                        }

Autocomplete
------------

The Autocomplete Widget displays a normal text with autocomplete feature. The user can type in a text and gets a list of the possible values from the `get_data` method. It is not possible to create new values. To create new values use the :py:func:`SuggestWidget()`.

The `set_entry_data` function is contains the data which is displayed/entrered into the actual autocomplete field. Whereas the self.data is the corresponding value. An entry is always a touple with ID and Value e.g. `(1, New)`. The self.data can be None if nothing matching is found in the data reutrn by the `get-data` function.

    .. py:function:: AutocompleteWidget()

        .. code:: bash

            epfl.fields.Suggest("on_change"=epflwidgetbase.EventType,
                                "get_data"=epflwidgetbase.MethodType,        # the function that gets the current input as parameter and
                                                                             # returns the matching possible values (list of tuples [(value, visual), ...])

                                "match_required"=(epflwidgetbase.BooleanType, False), # if true, the entered value must be from the "get_data"-method, so
                                                                                      # this ensures that the value is from the defined domain, but
                                                                                      # you can not "create" new values)

        The data in `get_data` can be defined as followed:

        .. code:: bash


            "get_data"="self.get_entry_data"

            def get_entry_data():
                return[(1, u"New"),(2, u"Used"), (3, "b-stock")]


Suggest
-------

The Suggest Widget displays a normal text-entry with autocomplete feature. In comparison to the autocomplete the suggest doesn't need a specific
and given value. Here the user has the possibility to create a new value.

The entry-data accessed by ``self.get_entry_data`` and ``self.set_entry_data`` is always a string. The entry-data corresponds to the "visual" of the select-box, so it is the data the user selects from the suggest-box or types in.
``self.data`` and the ``entry-data`` is never garanteed to correspond to each other, only if the user selects from the suggest-box.
The ``match_required`` option only checks on validation-phase that self.data and entry-data is match.
After a change of ``self.data`` you must call ``self.update_entry_data()`` to be sure that self.data and entry-data match.
This is done for you by ``form.set_data``.

    .. py:function:: SuggestWidget()

        .. code:: bash

            epfl.fields.Suggest(on_change=epflwidgetbase.EventType,
                                get_data=epflwidgetbase.MethodType,           # the function that gets the current input as parameter and
                                                                              # returns the matching possible values (list of tuples [(value, visual), ...])
                                                                              # This function must filter its results accordingly to the given input!
                                                                              # If None is given as input parameter, all existing data must be returned.
                                                                              # This is only the case if no get_visual-function is defined.

                                get_visual=epflwidgetbase.OptionalMethodType,    # this optional function returns the visual to a single given data-id.
                                                                                 # you should provide this function if your data-set is possibly very large
                                                                                 # and a get_data(None) would return too much data. (is is what epfl does
                                                                                 # if you do not declare a "get_visual"-function)

                                match_required=(epflwidgetbase.BooleanType, False),    # if true, the entered value must be from the "get_data"-method, so
                                                                                       # this ensures that the value is from the defined domain, but
                                                                                       # you can not "create" new values

                                new_value_func=epflwidgetbase.OptionalMethodType,    # this function is called, with the string entered into the field
                                                                                     # when "match_required" is false and the user
                                                                                     # enters a visual, that is not available in the list of possible values
                                                                                     # (returned by "get_data")
                                                                                     # The method MUST raise an ValueError with some error-message
                                                                                     # or return the new "value" for the given "visual" if it could not
                                                                                     # create the new value!)

        The SuggestWidget needs as an input a list with the entrys in touple format with the id and the value.

        .. code:: bash

            def get_entry_data():
                return[(1, u"New"),(2, u"Used"), (3, "b-stock")]







