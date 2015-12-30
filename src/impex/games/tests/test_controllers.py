from mock import MagicMock
from mock import sentinel

from impex.application.testing import ControllerCase
from impex.application.testing import cache

from ..controllers import GameListController


class TestGameListController(ControllerCase):
    _object_cls = GameListController

    @cache
    def mget_games(self):
        return self.pobject(self.object(), '_get_games')

    @cache
    def mmake_widgets(self):
        return self.pobject(self.object(), '_make_widgets')

    @cache
    def mgame_widget(self):
        return self.patch('impex.games.controllers.GameWidget')

    def test_make(self):
        self.mget_games()
        self.mmake_widgets()

        self.object().make()

        assert self.context() == {
            'games': self.mmake_widgets().return_value,
        }
        self.mmake_widgets().assert_called_once_with(
            self.mget_games().return_value
        )

    def test_get_games(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.mdrivers()

        result = self.object()._get_games()

        assert result == self.mdrivers().games.list.return_value
        self.mdrivers().games.list.assert_called_once_with(sentinel.event_id)

    def test_get_games_for_group(self):
        self.matchdict()['event_id'] = sentinel.event_id
        self.matchdict()['group_id'] = sentinel.group_id
        self.mdrivers()

        result = self.object()._get_games()

        assert result == self.mdrivers().games.list_for_group.return_value
        self.mdrivers().games.list_for_group.assert_called_once_with(
            sentinel.event_id,
            sentinel.group_id,
        )

    def test_make_widgets(self):
        obj = MagicMock()
        self.mgame_widget()

        result = list(self.object()._make_widgets([obj]))

        assert result == [self.mgame_widget().return_value]
        self.mgame_widget().assert_called_once_with(obj)
        self.mgame_widget().return_value.feed_request.assert_called_once_with(
            self.mrequest(),
        )
