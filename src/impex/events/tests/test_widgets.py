from mock import MagicMock

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import EventWidget


class TestBreadCrumbsWidget(RequestCase):

    @cache
    def mevent(self):
        return MagicMock()

    @cache
    def object(self):
        widget = EventWidget(self.mevent())
        widget.feed_request(self.mrequest())
        return widget

    def test_make(self):
        self.mdrivers()
        self.object().context = {}

        self.object().make()

        assert self.object().context == {
            'event': self.mevent(),
            'groups': self.mdrivers().groups.list_not_empty.return_value,
            'route_path': self.mrequest().route_path
        }
        self.mdrivers().groups.list_not_empty.assert_called_once_with(
            self.mevent().id,
        )
