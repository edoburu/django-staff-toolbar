django-staff-toolbar
====================

Displaying staff-only controls at a webpage.

Features:

* Linking to the admin page of the current object.
* Full configuration and customization of the displayed toolbar items.

This package has been tested in Django 1.5.


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


Contributing
============

This module is designed to be generic, and easy to plug into your site.
Pull requests and improvements are welcome!

If you have any other valuable contribution, suggestion or idea, please let us know as well!
