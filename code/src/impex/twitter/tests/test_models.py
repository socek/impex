from mock import MagicMock

from impaf.testing import cache
from impex.application.testing import RequestCase

from ..models import TwitterDriver


class TestTwitterDriver(RequestCase):

    @cache
    def object(self):
        obj = TwitterDriver()
        obj.feed_request(self.mrequest())
        return obj

    @cache
    def msettings(self,):
        return self.mregistry()['settings']

    @cache
    def mapi(self):
        self.object().api = MagicMock()
        return self.object().api

    def test_post_scores(self):
        def get_sum_for_quart(name, _):
            if name == 'left':
                return 5
            if name == 'right':
                return 10
        game = MagicMock()
        game.group.name = 'Grupa A'
        game.left.name = 'Lewa'
        game.right.name = 'Prawa'
        game.get_sum_for_quart.side_effect = get_sum_for_quart
        self.mapi()
        self.msettings()['main_url'] = 'http://scores.turniejkosza.pl'
        self.mroute_path().return_value = '/game/1'

        self.object().post_scores(game)

        self.mapi().PostUpdate.assert_called_once_with(
            'Wynik meczu: Grupa A - Lewa 5:10 Prawa #turniejkosza #wyniki http://scores.turniejkosza.pl/game/1',
        )
