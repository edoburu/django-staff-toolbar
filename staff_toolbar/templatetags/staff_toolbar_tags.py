from django.template import Library, Node
from django.template.loader import render_to_string
from django.utils.html import mark_safe
from staff_toolbar.loading import load_toolbar_item
from djangoappsettings import settings

register = Library()


@register.simple_tag(takes_context=True)
def render_staff_toolbar(context):
    """
    Renders the staff toolbar
    Usage:
        {% render_staff_toolbar %}
    """
    request = context['request']
    if not request.user.is_staff:
        return ''

    # Return the rendered template
    return render_to_string("staff_toolbar/toolbar.html", context_instance=context)


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


@register.tag()
def staff_toolbar(parser, token):
    """
    Iterates over the nodes in the toolbar tree, and renders the contained block for each node.
    This tag will recursively render children into the template variable {{ children }}.
    Usage:
        <ul>
            {% staff_toolbar %}
            <li>
                {{ node.name }}
                {% if not node.is_leaf_node %}
                <ul>
                    {{ children }}
                </ul>
                {% endif %}
            </li>
            {% end_staff_toolbar %}
        </ul>
    """

    template_nodes = parser.parse(('end_staff_toolbar',))
    parser.delete_first_token()
    return RecurseNode(template_nodes)


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


class RecurseNode(Node):

    def __init__(self, template_nodes):
        self.template = "staff_toolbar/toolbar.html"
        self.nodes = template_nodes

    def _render_node(self, context, import_path):
        bits = []
        context.push()
        item = load_toolbar_item(import_path)
        if hasattr(item, 'children'):
            for child in item.children:
                bits.append(self._render_node(context, child))
        context['item'] = item(context)
        children = mark_safe(''.join(bits))
        if children:
            context['children'] = mark_safe(''.join(bits))
        rendered = self.nodes.render(context)
        context.pop()
        return rendered

    def render(self, context):
        # For each item in settings, loop through and render
        bits = [self._render_node(context, item) for item in settings.STAFF_TOOLBAR_ITEMS]
        return ''.join(bits)
