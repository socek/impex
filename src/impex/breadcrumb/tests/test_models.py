from mock import sentinel

from ..models import BreadCrumbElement


class TestBreadCrumbElement(object):

    def test_init(self):
        element = BreadCrumbElement(
            sentinel.label,
            sentinel.url,
            sentinel.is_active,
        )

        assert element.label is sentinel.label
        assert element.url is sentinel.url
        assert element.is_active is sentinel.is_active
