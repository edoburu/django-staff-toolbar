from django.contrib.admin.templatetags.admin_urls import admin_urlname
from django.core.urlresolvers import reverse


class StaffUrlMixin(object):
    """
    Provide a ``view.get_admin_url`` variable in the template.
    """
    def get_staff_object(self):
        return getattr(self, 'object', None)

    def get_staff_url(self):
        """
        Return the Admin URL for the current view.
        By default, it uses the :func:`get_staff_object` function to base the URL on.
        """
        object = self.get_staff_object()
        if object is not None:
            # View is likely using SingleObjectMixin
            return reverse(admin_urlname(object._meta, 'change'), args=(object.pk,))

        model = _get_view_model(self)
        if model is not None:
            # View is likely using MultipleObjectMixin (e.g. ListView)
            return reverse(admin_urlname(object._meta, 'changelist'))

        return None



def _get_view_model(view):
    if view.model is not None:
        # If a model has been explicitly provided, use it
        return view.model
    elif hasattr(view, 'object') and view.object is not None:
        # If this view is operating on a single object, use the class of that object
        return view.object.__class__
    elif hasattr(view, 'get_queryset'):
        # Try to get a queryset and extract the model class from that
        return view.get_queryset().model
    else:
        return None
