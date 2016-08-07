from django.contrib.auth.models import AnonymousUser
from django.test import RequestFactory
from django.test import TestCase
from staff_toolbar import appsettings
from staff_toolbar.loading import get_toolbar_root


def get_dummy_request():
    """
    Returns a Request instance.
    """
    request = RequestFactory().get("/", HTTP_HOST='example.org')
    request.session = {}
    request.user = AnonymousUser()
    return request


class StaffToolbarTests(TestCase):
    """
    Staff toolbar test
    """

    def test_loading(self):
        root = get_toolbar_root()

        self.assertEqual(len(root.children), len(appsettings.STAFF_TOOLBAR_ITEMS))

        request = get_dummy_request()
        html = root(request, {})
        self.assertHTMLEqual(
            html,
            '''
            <div class="toolbar-title">Staff features</div>
            <ul>
                <li><a href="/admin/">Admin dashboard</a></li>
                <li><a href="/admin/logout/">Logout</a></li>
            </ul>
            '''
        )
