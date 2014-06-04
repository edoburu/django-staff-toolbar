from django.template import Library, Node
from django.utils.html import format_html
from staff_toolbar.loading import get_toolbar_root

register = Library()

toolbar_root = get_toolbar_root()


@register.simple_tag(takes_context=True)
def staff_toolbar(context):
    """
    Display the staff toolbar
    :param context:
    :type context:
    :return:
    :rtype:
    """
    request = context['request']
    if not request.user.is_staff:
        return u''

    toolbar_html = toolbar_root(request, context)
    return format_html(u'<nav id="django-staff-toolbar">{0}</nav>', toolbar_html)


@register.simple_tag(takes_context=True)
def set_staff_object(context, object):
    """
    Assign an object to be the "main object" of this page.
    Example::

        {% set_staff_object page %}
    """
    request = context['request']
    request.staff_object = object
    return u''


@register.tag
def set_staff_url(parser, token):
    """
    Assign an URL to be the "admin link" of this page.
    Example::

        {% set_staff_url %}{% url 'admin:fluent_pages_page_change' page.id %}{% end_set_staff_url %}
    """
    nodelist = parser.parse(('end_set_staff_url',))
    parser.delete_first_token()
    return AdminUrlNode(nodelist)


class AdminUrlNode(Node):
    def __init__(self, nodelist):
        self.nodelist = nodelist

    def render(self, context):
        url = self.nodelist.render(context)
        context['request'].staff_url = url
        return u''
