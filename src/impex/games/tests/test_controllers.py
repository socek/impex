from mock import MagicMock
from mock import call

from impex.application.testing import ControllerCase
from impex.application.testing import cache

from ..controllers import GameListController


class TestGameListController(ControllerCase):
    _object_cls = GameListController

    @cache
    def mget_games(self):
        return self.pobject(self.object(), '_get_games')

    @cache
    def mgame_widget(self):
        return self.patch('impex.games.controllers.GameWidget')

    def test_make(self):
        self.mget_games()

        self.object().make()

        assert self.context() == {
            'games': self.mget_games().return_value,
        }

    def test_set_breadcrumb(self):
        self.mroute_path()
        mock = MagicMock()
        self.object().set_crumbs(mock)

        mock.add_breadcrumb.assert_has_calls(
            [
                call(
                    'Główna',
                    self.mroute_path().return_value,
                ),
                call(
                    'Mecze',
                    None,
                    True,
                ),
            ]
        )

    def test_get_games(self):
        obj = MagicMock()
        self.mdrivers().games.list.return_value = [obj]
        self.mgame_widget()

        result = list(self.object()._get_games())

        assert result == [self.mgame_widget().return_value]
        self.mgame_widget().assert_called_once_with(obj)
        self.mgame_widget().return_value.feed_request.assert_called_once_with(
            self.mrequest(),
        )
