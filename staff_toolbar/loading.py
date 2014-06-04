"""
The internal machinery to load the toolbar items.
"""
import inspect
import traceback
import sys
from django.core.exceptions import ImproperlyConfigured
from staff_toolbar import appsettings
from staff_toolbar.items import RootNode, Group

try:
    from importlib import import_module
except ImportError:
    from django.utils.importlib import import_module  # Python 2.6 compatibility

_toolbar_root = None


__all__ = (
    'get_toolbar_root',
    'load_toolbar_item'
)


def get_toolbar_root():
    """
    Init on demand.
    :rtype RootNode:
    """
    global _toolbar_root
    if _toolbar_root is None:
        items = [load_toolbar_item(item) for item in appsettings.STAFF_TOOLBAR_ITEMS]
        _toolbar_root = RootNode(*items)
    return _toolbar_root


def load_toolbar_item(import_path, *args, **kwargs):
    """
    Load an item in the toolbar
    :param import_path: the dotted python path to class or function.
    :param args: For classes, any arguments to pass to the constructor.
    :param kwargs: For classes, any keyword arguments to pass to the constructor.
    """
    if isinstance(import_path, (tuple, list)):
        children = [load_toolbar_item(path) for path in import_path]
        return Group(*children)
    elif isinstance(import_path, basestring):
        symbol = _import_symbol(import_path, 'STAFF_TOOLBAR_ITEMS')
    else:
        symbol = import_path

    if inspect.isclass(symbol):
        # Instantiate the class.
        symbol = symbol(*args, **kwargs)

    if not callable(symbol):
        raise ImproperlyConfigured("The {0} in {1} is not callable!".format(import_path, 'STAFF_TOOLBAR_ITEMS'))

    return symbol


def _import_symbol(import_path, setting_name):
    """
    Import a class or function by name.
    """
    mod_name, class_name = import_path.rsplit('.', 1)

    # import module
    try:
        mod = import_module(mod_name)
        cls = getattr(mod, class_name)
    except ImportError, e:
        __, __, exc_traceback = sys.exc_info()
        frames = traceback.extract_tb(exc_traceback)
        if len(frames) > 1:
            raise   # import error is a level deeper.

        raise ImproperlyConfigured("{0} does not point to an existing class: {1}".format(setting_name, import_path))
    except AttributeError:
        raise ImproperlyConfigured("{0} does not point to an existing class: {1}".format(setting_name, import_path))

    return cls
