Permissions via ACL
===================
EPFL exposes the powerful pyramid ACL implementation in :class:`~solute.epfl.core.epflassets.EPFLView`. Consider the
following basic scenario:
 1. a login page,
 2. a home page with some secret information,
 3. a forbidden page with a warning.

Setting up ACL
--------------
Using the pyramid_epfl_starter scaffold you have already setup pyramid to use an ACLAuthorizationPolicy.
:class:`~solute.epfl.core.epflassets.EPFLView` complements that by setting a RootFactory with a global set of ACLs. In
order to populate that set :meth:`~solute.epfl.core.epflassets.EPFLView.register_acl`.
