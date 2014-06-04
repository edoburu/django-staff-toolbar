from django.conf import settings

STAFF_TOOLBAR_ITEMS = getattr(settings, 'STAFF_TOOLBAR_ITEMS', (
    'staff_toolbar.items.AdminIndexLink',
    'staff_toolbar.items.ChangeObjectLink',
    'staff_toolbar.items.LogoutLink',
))
