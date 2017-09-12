from mock import MagicMock
from mock import sentinel

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import BreadCrumbsWidget


class TestBreadCrumbsWidget(RequestCase):

    @cache
    def controller(self):
        return MagicMock()

    @cache
    def object(self):
        return BreadCrumbsWidget(self.controller())

    @cache
    def mbreadcrumb(self):
        return self.patch('impex.breadcrumb.widgets.BreadCrumb')

    def test_make(self):
        self.controller().crumbs = sentinel.name
        self.mbreadcrumb()
        self.object().context = {}
        self.object().feed_request(self.mrequest())
        self.object().make()

        assert self.object().context == {
            'bread': self.mbreadcrumb().return_value,
            'name': sentinel.name,
            'crumbs': (
                self.mbreadcrumb().return_value.get_crumbs_for.return_value
            ),
            'request': self.mrequest(),
            'widget': self.object(),
        }
        self.mbreadcrumb().return_value.get_crumbs_for.assert_called_once_with(
            sentinel.name
        )
