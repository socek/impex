from impex.application.testing import RequestCase
from impex.application.testing import cache

from ..base import TabWidget


class TestTabList(RequestCase):

    @cache
    def tab_widget(self):
        widget = TabWidget()
        widget.feed_request(self.mrequest())
        return widget

    def test_make(self):
        self.tab_widget().name = 'myname'

        self.tab_widget().make()

        assert self.tab_widget().context == {
            'name': 'myname',
            'request': self.mrequest(),
            'widget': self.tab_widget(),
        }

    def test_to_dict(self):
        self.context()
        self.tab_widget().name = 'myname'
        self.tab_widget().speed = 5

        assert self.tab_widget().to_dict() == {
            'name': 'myname',
            'speed': 5,
        }
