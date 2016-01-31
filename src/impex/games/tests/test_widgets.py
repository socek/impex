from mock import MagicMock
from mock import sentinel

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import GameWidget


class TestGameWidget(RequestCase):

    @cache
    def game(self):
        return MagicMock()

    @cache
    def object(self):
        widget = GameWidget(self.game())
        widget.feed_request(self.mrequest())
        return widget

    def test_simple(self):
        self.object().context = {}
        self.mroute_path()
        self.mmatchdict()['event_id'] = sentinel.event_id

        self.object().make()

        assert self.object().context == {
            'game': self.game(),
            'edit_url': self.mroute_path().return_value,
        }
        self.mroute_path().assert_called_once_with(
            'games:admin:edit_scores',
            event_id=sentinel.event_id,
            game_id=self.game().id,
        )
