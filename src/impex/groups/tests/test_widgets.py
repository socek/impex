from mock import MagicMock

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import GroupHighScoreWidget


class TestGroupHighScoreWidget(RequestCase):

    @cache
    def mgroup(self):
        return MagicMock()

    @cache
    def mevent(self):
        return MagicMock()

    @cache
    def object(self):
        obj = GroupHighScoreWidget(self.mevent(), self.mgroup())
        obj.feed_request(self.mrequest())
        return obj

    @cache
    def mmake_scores(self):
        return self.pobject(self.object(), 'make_scores')

    def test_when_empty(self):
        game = self._create_game('left', 5, 'right', 10)
        game.status = game.STATUS_RUNNING
        self.mdrivers().games.list_for_group.return_value = [game]

        assert list(self.object().make_scores()) == [
            {'games': 0, 'name': 'left', 'points': 0, 'smallpoints': 0, 'wins': 0},
            {'games': 0, 'name': 'right', 'points': 0, 'smallpoints': 0, 'wins': 0},
        ]

    def test_simple(self):
        self.mdrivers().games.list_for_group.return_value = [
            self._create_game(1, 5, 2, 10),
            self._create_game(2, 10, 3, 5),
            self._create_game(1, 15, 3, 10),
            self._create_game(4, 5, 2, 5)
        ]

        assert list(self.object().make_scores()) == [
            {'games': 3, 'name': '2', 'points': 5, 'smallpoints': 25, 'wins': 2},
            {'games': 2, 'name': '1', 'points': 2, 'smallpoints': 20, 'wins': 1},
            {'games': 1, 'name': '4', 'points': 1, 'smallpoints': 5, 'wins': 0},
            {'games': 2, 'name': '3', 'points': 0, 'smallpoints': 15, 'wins': 0}
        ]

    def _create_game(self, left_id, left_score, right_id, right_score):
        def get_sum_for_quart(side, _):
            if side == 'left':
                return left_score
            else:
                return right_score
        game = MagicMock()
        left = game.left
        left.id = left_id
        left.name = str(left_id)

        right = game.right
        right.id = right_id
        right.name = str(right_id)

        game.status = game.STATUS_ENDED
        game.get_sum_for_quart.side_effect = get_sum_for_quart
        return game

    def test_make(self):
        self.mmake_scores()
        self.object().context = {}

        self.object().make()

        assert self.object().context == {
            'teams': self.mmake_scores().return_value,
        }
