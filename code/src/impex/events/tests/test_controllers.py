from mock import MagicMock

from impex.application.testing import ControllerCase
from impex.application.testing import cache

from ..controllers import EventListController


class TestEventListController(ControllerCase):
    _object_cls = EventListController

    @cache
    def mevent_widget(self):
        return self.patch('impex.events.controllers.EventWidget')

    @cache
    def mgame(self):
        game = MagicMock()
        self.mdrivers().events.list_for_user.return_value = [game]
        return game

    def test_make(self):
        self.mgame()
        self.mevent_widget()

        self.object().make()

        events = list(self.context()['events'])

        widget = self.mevent_widget().return_value
        assert events == [widget]
        self.mevent_widget().assert_called_once_with(self.mgame())
        widget.feed_request.assert_called_once_with(self.mrequest())
