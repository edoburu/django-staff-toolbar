import mock
import os
import logging
logging.disable(logging.CRITICAL)

from bs4 import BeautifulSoup
from django.core.urlresolvers import reverse_lazy
from django.template import Template, Context
from django.test import TestCase
from django.test.utils import override_settings
from django.utils.translation import ugettext_lazy as _
from staff_toolbar import toolbar_item, toolbar_title


@override_settings(TEMPLATE_DIRS=('%s/templates' % os.path.abspath(os.path.dirname(__file__)),))
class StaffToolbarTestCase(TestCase):
    def setUp(self):
        self.request = mock.Mock()
        self.request.user = mock.Mock()
        self.request.user.configure_mock(**{'is_staff.return_value': True, })
        self.context = Context({'request': self.request})
        self.template = "{% load staff_toolbar_tags %}{% render_staff_toolbar %}"

    @override_settings(STAFF_TOOLBAR_ITEMS=(
        'staff_toolbar.items.AdminIndexLink',
        'staff_toolbar.items.ChangeObjectLink',
        'staff_toolbar.items.LogoutLink',
    ))
    def test_simple_toolbar(self):
        rendered = Template(self.template).render(self.context)
        soup = BeautifulSoup(rendered)
        lis = soup.find_all('li')
        self.assertEqual(len(lis), 3)
        lis = [str(l).strip() for l in lis]
        self.assertEqual(lis[0], '<li>\n<a href="/admin/">Admin dashboard</a>\n</li>')
        self.assertRegexpMatches(lis[1], 'Change')
        self.assertEqual(lis[2], '<li>\n<a href="/admin/logout/">Logout</a>\n</li>')

    @override_settings(STAFF_TOOLBAR_ITEMS=(
        'staff_toolbar.items.AdminIndexLink',
        'staff_toolbar.items.ChangeObjectLink', (
            toolbar_title(_("User")),
            toolbar_item('staff_toolbar.items.Link', url=reverse_lazy('admin:password_change'), title=_("Change password")),
            'staff_toolbar.items.LogoutLink',
        )
    ))
    def test_children_toolbar(self):
        rendered = Template(self.template).render(self.context)
        soup = BeautifulSoup(rendered)
        lis = soup.find_all('li')
        ls = [str(l).strip() for l in lis]
        self.assertEqual(ls[0], '<li>\n<a href="/admin/">Admin dashboard</a>\n</li>')
        self.assertRegexpMatches(ls[1], 'Change')

        ls = lis[2].find_all('ul')[0].find_all('li')
        ls = [str(l).replace('\n', '') for l in ls]
        self.assertEqual(ls[0], '<li><div class="toolbar-title">User</div></li>')
        self.assertEqual(ls[1], '<li><a href="/admin/password_change/">Change password</a></li>')
        self.assertEqual(ls[2], '<li><a href="/admin/logout/">Logout</a></li>')

    @override_settings(STAFF_TOOLBAR_ITEMS=(
        'staff_toolbar.items.AdminIndexLink', (
            toolbar_title(_("User")), (
                'staff_toolbar.items.AdminIndexLink',
            ),
        )
    ))
    def test_complex_toolbar(self):
        rendered = Template(self.template).render(self.context)
        soup = BeautifulSoup(rendered)
        lis = soup.find_all('li')
        ls = [str(l).strip() for l in lis]
        self.assertEqual(ls[0], '<li>\n<a href="/admin/">Admin dashboard</a>\n</li>')

        lis = lis[1].find_all('li')
        ls = [str(l).strip() for l in lis]
        self.assertEqual(ls[0], '<li>\n<div class="toolbar-title">User</div>\n</li>')

        lis = lis[1].find_all('li')
        ls = [str(l).strip() for l in lis]
        self.assertEqual(ls[0], '<li>\n<a href="/admin/">Admin dashboard</a>\n</li>')
