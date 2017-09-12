from mock import MagicMock
from mock import sentinel

from impaf.testing import cache

from impex.application.testing import RequestCase

from ..models import BreadCrumb
from ..models import BreadCrumbElement
from ..models import EventElement
from ..models import GameListElement


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
        element.feed_request(None)

        assert element.get_url() is None

    def test_get_url(self):
        element = BreadCrumbElement('label', lambda reg: reg)
        element.feed_request(sentinel.request)

        assert element.get_url() == sentinel.request


class TestBreadCrumb(object):

    @cache
    def bread(self):
        return BreadCrumb()

    def test_simple(self):
        generator = list(self.bread().get_crumbs_for('admin:home'))

        assert generator[0] == self.bread().data['home']
        assert generator[1] == self.bread().data['admin:home']

    def test_on_empty_key(self):
        for element in self.bread().get_crumbs_for(None):
            # generator should be empty
            assert False

    def test_urls_sanity_check(self):
        for key, value in self.bread().data.items():
            request = MagicMock()
            value.feed_request(request)
            value.get_url() == request.route_path.return_value

    def test_breadcrumb(self):
        request = MagicMock()
        obj = MagicMock()
        self.bread().data = {'key': obj}
        self.bread().feed_request(request)
        obj.feed_request.assert_called_once_with(request)


class TestEventElement(RequestCase):

    @cache
    def object(self):
        return EventElement()

    def test_simple(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.object().feed_request(self.mrequest())
        self.mdrivers()

        assert (
            self.object().label
            == self.mdrivers().events.get_by_id.return_value.name
        )
        self.mdrivers().events.get_by_id.assert_called_once_with(
            sentinel.event_id,
        )


class TestGameListElement(RequestCase):

    @cache
    def object(self):
        obj = GameListElement()
        obj.feed_request(self.mrequest())
        return obj

    def test_label(self):
        self.matchdict()

        assert self.object().label == 'Mecze'

    def test_label_for_group(self):
        self.matchdict()['group_id'] = sentinel.group_id
        self.mdrivers()

        assert (
            self.object().label
            == self.mdrivers().groups.get_by_id.return_value.name
        )

    def test_url(self):
        self.matchdict()['event_id'] = sentinel.event_id
        assert (
            self.object().get_url()
            == self.mrequest().route_path.return_value
        )
        self.mrequest().route_path.assert_called_once_with(
            'games:list',
            event_id=sentinel.event_id,
        )

    def test_url_for_group(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['group_id'] = sentinel.group_id
        assert (
            self.object().get_url()
            == self.mrequest().route_path.return_value
        )
        self.mrequest().route_path.assert_called_once_with(
            'games:group_list',
            event_id=sentinel.event_id,
            group_id=sentinel.group_id,
        )
