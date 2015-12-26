from mock import MagicMock
from mock import sentinel

from impaf.testing import cache

from ..models import BreadCrumb
from ..models import BreadCrumbElement


class TestBreadCrumbElement(object):

    def test_init(self):
        element = BreadCrumbElement(
            sentinel.label,
            sentinel.url,
            sentinel.parent,
        )

        assert element.label is sentinel.label
        assert element.url is sentinel.url
        assert element.parent is sentinel.parent

    def test_get_url_on_empty(self):
        element = BreadCrumbElement('label', None)

        assert element.get_url(None) is None

    def test_get_url(self):
        element = BreadCrumbElement('label', lambda reg: reg)

        assert element.get_url(sentinel.request) == sentinel.request


class TestBreadCrumb(object):

    @cache
    def bread(self):
        return BreadCrumb()

    def test_simple(self):
        generator = list(self.bread().get_crumbs_for('empty:admin'))

        assert generator[0] == self.bread().data['home']
        assert generator[1] == self.bread().data['empty:admin']

    def test_on_empty_key(self):
        for element in self.bread().get_crumbs_for(None):
            # generator should be empty
            assert False

    def test_urls_sanity_check(self):
        for key, value in self.bread().data.items():
            request = MagicMock()
            value.get_url(request) == request.route_path.return_value
