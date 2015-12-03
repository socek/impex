from mock import MagicMock

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

    def test_make(self):
        self.object().context = {}
        self.object().make()

        self.controller().set_crumbs.assert_called_once_with(self.object())
        assert self.object().context == {'crumbs': []}

    def test_make_when_no_set_crumbs_method(self):
        obj = BreadCrumbsWidget(None)
        obj.context = {}

        obj.make()

        assert obj.context == {'crumbs': []}

    def test_add_breadcrumb(self):
        self.object().context = {'crumbs': []}
        self.object().add_breadcrumb('label', 'url', True)

        crumb = self.object().context['crumbs'][0]
        assert crumb.label == 'label'
        assert crumb.url == 'url'
        assert crumb.is_active is True
