from mock import MagicMock

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import GameWidget


class TestGameWidget(RequestCase):

    @cache
    def game(self):
        return MagicMock()

    @cache
    def object(self):
        return GameWidget(self.game())

    def test_simple(self):
        self.object().context = {}
        self.object().make()

        assert self.object().context == {'game': self.game()}
