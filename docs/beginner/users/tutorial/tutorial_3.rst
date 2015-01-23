.. _tutorial_3:

Tutorial Part 3: Authentication & Authorization
===============================================

In the following part of the tutorial, we show how rights management works in EPFL.
We are going to build a view that provides a login dialog and UI elements which should only
be visible upon login.

We start with a basic empty page and add two boxes to the page:

.. code-block:: python

	class HomeRoot(epfl.components.CardinalLayout):
	
	    def init_struct(self):
	        self.node_list.extend([Box(title='This box should only be displayed to authenticated users.'),
	                               Box(title='This box should only be displayed to authenticated admin users.')])


	@view_config(route_name='home')
	class HomePage(epfl.Page):
	    root_node = HomeRoot(
	        constrained=True, node_list=[NavLayout(slot='north', title='Demo Notes App')])

Currently, this view only displayes the two boxes to everyone. Lets add authentication:
We do this by simply adding a login dialog to the same page:

.. code-block:: python

	class Login(Box):
	
	    title = 'Login'
	
	    node_list = [cfForm(cid='login_form',
	                        node_list=[cfText(label='Username',
	                                          name='username'),
	                                   cfText(label='Password',
	                                          name='password',
	                                          input_type='password'),
	                                   cfButton(value='Login',
	                                            event_name='login')])]
	    def handle_login(self):
	        pass
	
	class HomeRoot(epfl.components.CardinalLayout):
	
	    def init_struct(self):
	        self.node_list.extend([Login(),
	                               Box(title='This box should only be displayed to authenticated users.'),
	                               Box(title='This box should only be displayed to authenticated admin users.')])

Let's add authentication checks.
We simple add a hard-coded dict of two users to our Login box, and check in the handle_login method whether the form is valid and the
corresponding users can be found in our user dict. In this case, we know that the user has passed valid credentials and can authenticate
the user.

Note that you should normally perform this operation on your authentication backend, and never store sensitive user information such as passwords as plain text!
Your view should then use its model to access the authentication logic.

.. code-block:: python

	class Login(Box):
	    
	    users = {'admin': 'abcdefg',
	             'someuser': '12345'}
	
	    ...
	    
	    def handle_login(self):
	        if not self.page.login_form.validate():
	            return
	        values = self.page.login_form.get_values()
	
	        if self.users.get(values['username'], None) != values['password']:
	            self.show_fading_message('Invalid authentication details!', 'error')
	            return
	
	        self.page.reload()

Now the user gets an error message if the credentials are invalid, but nothing happens if they are valid.
To authenticate the user on the current session, we call remember() on the page with the user id of the user to authenticate:

.. code-block:: python

	class Login(Box):
	
	    ...
	    
	    def handle_login(self):
	        ...
	        self.page.remember(values['username'])
	        self.page.reload()

The actual authentication logic is handled by pyramid's authentication framework.
Now the session knows when an authenticated user has called the view.
Let's hide the login dialog in such as case.
For this, we use the EPFL @epfl_acl annotation.
This annotation can be put before component classes or methods to indicate which parts of the view should be displayed to whom, 
and which operations should be allowed.

.. code-block:: python

	from solute.epfl.core.epflassets import epfl_acl
	
	@epfl_acl(['access',
	           (False, 'system.Authenticated', 'access')])
	class Login(Box):
	
	    ...
	
After adding the ACL, the login dialog is not displayed anymore once valid credentials have been submitted.
The given ACL can be read as follows:

* By default, anyone can access the Login dialog
* If the requesting object has the role "system.Authenticated" (which is set upon calling remember() on the page), the operation "access" is not allowed, hence the dialog is hidden from the view.

Let's add logout functionality. We add a logout box with a logout button that is only visible for authenticated users, and call forget() on the page (
the counterpart of page.remember()) upon a click on the logout button: 

.. code-block:: python

	@epfl_acl([('system.Authenticated', 'access')])
	class Logout(Box):
	
	    title = 'Logout'
	    node_list = [cfButton(value='Logout',
	                          event_name='logout')]
	
	    def handle_logout(self):
	        self.page.forget()
	        self.page.reload()
	
	class HomeRoot(epfl.components.CardinalLayout):

	    def init_struct(self):
	        self.node_list.extend([Login(),
	                               Logout(),
	                               Box(title='This box should only be displayed to authenticated users.'),
	                               Box(title='This box should only be displayed to authenticated admin users.')])

Finally, we only have to set the correct rights to the two boxes on the page, which are currently displayed to everyone.
Since ACLs can only be set for classes or methods, but not for object instances, we have to provide own classes the
two boxes in order to provide ACLs for them:

.. code-block:: python

	@epfl_acl([('system.Authenticated', 'access')])
	class UserBox(Box):
	
	    title='This box should only be displayed to authenticated users.'
	
	@epfl_acl([('admin', 'access')])
	class AdminBox(Box):
	
	    title='This box should only be displayed to authenticated admin users.'
	
	class HomeRoot(epfl.components.CardinalLayout):
	
	        def init_struct(self):
	            self.node_list.extend([Login(),
	                                   Logout(),
	                                   UserBox(),
	                                   AdminBox()])

Now, only the user box is displayed for all authenticated user, and since the admin box has a more restrictive ACL, it is only displayed when the admin
user is authenticated.  