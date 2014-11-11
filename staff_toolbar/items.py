"""
These are the items that can be added to the staff toolbar.
"""
from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse, reverse_lazy
from django.utils.encoding import force_text
from django.utils.translation import ugettext_lazy as _
from django.utils.html import format_html

__all__ = (
    'Group',
    'RootNode',
    'Link',
)


class Title(object):
    """
    A title in the toolbar.
    """
    def __init__(self, title):
        self.title = title

    def __call__(self, context):
        return format_html(u'<div class="toolbar-title">{0}</div>', self.title)


class Literal(object):
    """
    A literal object, that is outputted as-is.
    Use ``format_html()`` or ``mark_safe()`` to output literal HTML.
    """
    def __init__(self, title):
        self.title = title

    def __call__(self, context):
        return self.title


class Group(object):
    """
    A group of items
    """
    title = None

    def __init__(self, *children, **kwargs):
        self.children = list(children)
        self.title = kwargs.get('title', self.title)

    def __call__(self, context):
        return ''


class RootNode(Group):
    """
    The root node for the toolbar.
    """
    title = _("Staff features")


class Link(object):
    """
    Add a hard-coded link in the toolbar.
    """
    # Allow to define class-level defaults.
    url = None
    title = None

    def __init__(self, url=None, title=None):
        # Assign class-level values to 'self' if nothing is passed.
        self.url = url or self.url
        self.title = title or self.title

    def __call__(self, context):
        linkdata = self.get_link(context)
        if linkdata:
            return format_html(u'<a href="{0}">{1}</a>', *linkdata)
        else:
            return None

    def get_link(self, context):
        return (self.url, self.title)


class AdminIndexLink(Link):
    """
    A link to the admin index.
    """
    url = reverse_lazy('admin:index')
    title = _("Admin dashboard")


class ChangeObjectLink(Link):
    """
    Display a link to the admin of the current page.
    It tries to fetch the URL using:

    * ``{% set_staff_object ... %}``
    * ``{% set_staff_url %}...{% end_set_staff_url %}``
    * ``request.staff_url``
    * ``request.staff_object``
    * ``view.get_staff_object()`
    * ``view.get_staff_url()`
    """
    def get_link(self, context):
        request = context['request']
        # When `staff_object` is used, take that information,
        object = getattr(request, 'staff_object', None)
        url = getattr(request, 'staff_url', None)

        if not object and not url:
            # If the information was not passed in the template,
            # the view can also be queried.
            view = context.get('view')
            if view is not None:
                # Implementing StaffUrlMixin
                if hasattr(view, 'get_staff_url'):
                    url = view.get_staff_url()
                if hasattr(view, 'get_staff_object'):
                    object = view.get_staff_object()

            if not object:
                # Last resort, try to find the object in the context or view.
                object = get_object(context)

        if object and url:
            # URL and object, use that!
            return (url, _admin_title(object))
        if object:
            # No URL, take default
            return (_admin_url(object), _admin_title(object))
        if url:
            # URL only, default title
            return (url, _("Edit content"))

        return None


class LogoutLink(Link):
    """
    A logoff link.
    """
    url = reverse_lazy('admin:logout')
    title = _("Logout")


def get_object(context):
    """
    Get an object from the context or view.
    """
    object = None

    view = context.get('view')
    if view:
        # View is more reliable then an 'object' variable in the context.
        # Works if this is a SingleObjectMixin
        object = getattr(view, 'object', None)

    if object is None:
        object = context.get('object', None)

    return object


def _admin_url(object):
    return reverse(admin_urlname(object._meta, 'change'), args=(object.pk,))


def _admin_title(object):
    return _('Change %s') % force_text(object._meta.verbose_name)
