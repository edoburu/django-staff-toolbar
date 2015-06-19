django-staff-toolbar
====================

Displaying staff-only controls at a webpage.

Features:

* Linking to the admin page of the current object.
* Full configuration of the displayed toolbar items.
* API for adding custom menu items.

.. image:: https://github.com/edoburu/django-staff-toolbar/raw/master/docs/images/staff_toolbar.png
   :width: 142px
   :height: 136px
   :alt: django-staff-toolbar preview


Installation
============

First install the module, preferably in a virtual environment::

    git clone https://github.com/edoburu/django-staff-toolbar.git
    cd django-staff-toolbar
    pip install .


Configuration
-------------

Add the application to ``settings.py``::

    INSTALLED_APPS += (
        'staff_toolbar',
    )

Make sure the ``django.core.context_processors.request`` is included in ``TEMPLATE_CONTEXT_PROCESSORS``.

Add the HTML widget to the template::

    {% load staff_toolbar_tags %}

    {% staff_toolbar %}

Make sure the layout is loaded in the template::

    <link rel="stylesheet" type="text/css" href="{{ STATIC_URL }}staff_toolbar/staff_toolbar.css" />

Layout
------

By default, a simple layout is included.
You can change this layout to your own liking.

The source SASS file is included, making it easier to
integrate this into your project stylesheets when needed.


Customizing the admin URL
=========================

The admin URL is auto-detected using:

* The ``object`` variable in the template.
* The ``view.object`` variable in the template.

In some cases, this is not sufficient. When the auto-detected "Change object"
link does not point to the right page, this can be resolved using two methods:

Using the view
--------------

When your class-based-view implements ``staff_toolbar.views.StaffUrlMixin``,
that information will be used to render the proper "Change object" link.

This requires Django 1.5, which exports the ``view`` variable to the template.

Using the template
------------------

In the template, you can include::

    {% set_staff_object page %}

When needed, the URL can also be set::

    {% set_staff_url %}{% url 'dashboard:catalogue-product' object.id %}{% end_set_staff_url %}


Customizing the menu
====================

The default menu settings are::

    STAFF_TOOLBAR_ITEMS = (
        'staff_toolbar.items.AdminIndexLink',
        'staff_toolbar.items.ChangeObjectLink',
        'staff_toolbar.items.LogoutLink',
    )

Each line represents a callable, which is called using ``(request, context)``.
When a tuple is included, this is converted into a new ``Group`` object,
causing an additional ``<ul>`` tag to appear in the output.

A more complex example::

    from django.core.urlresolvers import reverse_lazy
    from django.utils.translation import ugettext_lazy as _
    from staff_toolbar import toolbar_item, toolbar_title, toolbar_literal

    STAFF_TOOLBAR_ITEMS = (
        'staff_toolbar.items.AdminIndexLink',
        'staff_toolbar.items.ChangeObjectLink',
        (
            toolbar_title(_("User")),
            toolbar_item('staff_toolbar.items.Link', url=reverse_lazy('admin:password_change'), title=_("Change password")),
            'staff_toolbar.items.LogoutLink',
        )
    )

The ``toolbar_title()`` and ``toolbar_item()`` functions allow to pass additional arguments
to the items, without having to load them already in the settings.

It's also perfectly possible to instantiate the actual classes directly,
however this may risk import errors as it causes your settings module to load a lot of other code.
The following is functionally equivalent to the previous example::

    from django.core.urlresolvers import reverse_lazy
    from django.utils.translation import ugettext_lazy as _
    from staff_toolbar.items import AdminIndexLink, ChangeObjectLink, Group, ToolbarTitle, Link, LogoutLink

    STAFF_TOOLBAR_ITEMS = (
        AdminIndexLink(),
        ChangeObjectLink(),
        Group(
            ToolbarTitle(_("User")),
            Link(url=reverse_lazy('admin:password_change'), title=_("Change password")),
            LogoutLink(),
        )
    )


Caveats
=======

For HTTPS sites with ``SESSION_COOKIE_SECURE = True`` the toolbar obviously
won't show up in the standard pages that are served by HTTP.

Either display all pages on HTTPS (which is the Right Way™ after all),
or please provide a good pull request that solves this nicely for mixed sites.


Contributing
============

This module is designed to be generic, and easy to plug into your site.
Pull requests and improvements are welcome!

If you have any other valuable contribution, suggestion or idea, please let us know as well!
