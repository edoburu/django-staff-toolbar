# following PEP 440

__version__ = "1.0.1"

__all__ = (
    'toolbar_title',
    'toolbar_item',
    'toolbar_literal',
)


def toolbar_title(title):
    """
    Define a title to be included in the toolbar.
    """
    return LazyToolbarItem('staff_toolbar.items.Title', title)


def toolbar_literal(title):
    """
    Define a literal text to be included in the toolbar.
    """
    return LazyToolbarItem('staff_toolbar.items.Literal', title)


def toolbar_item(callable_path, *args, **kwargs):
    """
    Defining a toolbar item in the settings that also received arguments.
    It won't be loaded until the toolbar is actually rendered.
    """
    return LazyToolbarItem(callable_path, *args, **kwargs)


class LazyToolbarItem(object):
    """
    Internal mechanism to support lazy-loaded toolbar items in the settings.
    """
    def __init__(self, import_path, *args, **kwargs):
        self.import_path = import_path
        self.args = args
        self.kwargs = kwargs
        self.real_instance = None

    def __call__(self, request, context):
        if self.real_instance is None:
            # Init on demand.
            from staff_toolbar.loading import load_toolbar_item
            self.real_instance = load_toolbar_item(self.import_path, *self.args, **self.kwargs)

        return self.real_instance(request, context)
