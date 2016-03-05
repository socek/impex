from mock import MagicMock

from impaf.testing.cache import cache

from impex.application.testing import RequestCase

from ..widgets import GroupHighScoreWidget
from ..widgets import LadderWidget


class ScoreCase(RequestCase):

    @cache
    def mevent(self):
        return MagicMock()

    @cache
    def mgroup(self):
        return MagicMock()

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

        if right_id:
            right = game.right
            right.id = right_id
            right.name = str(right_id)
        else:
            game.right = None

        game.status = game.STATUS_ENDED
        game.is_ended = True
        game.get_sum_for_quart.side_effect = get_sum_for_quart
        return game


class TestGroupHighScoreWidget(ScoreCase):

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

        assert sorted(list(self.object().make_scores()), key=lambda x: x['name']) == [
            {'games': 0, 'name': 'left', 'points': 0, 'smallpoints': 0, 'wins': 0, 'second_points': 0},
            {'games': 0, 'name': 'right', 'points': 0, 'smallpoints': 0, 'wins': 0, 'second_points': 0},
        ]

    def test_simple(self):
        self.mdrivers().games.list_for_group.return_value = [
            self._create_game(1, 5, 2, 10),
            self._create_game(2, 10, 3, 5),
            self._create_game(1, 15, 3, 10),
            self._create_game(4, 5, 2, 5),
            self._create_game(4, 5, None, None),
        ]

        assert list(self.object().make_scores()) == [
            {'games': 3, 'name': '2', 'points': 5, 'smallpoints': 25, 'wins': 2, 'second_points': 0},
            {'games': 2, 'name': '1', 'points': 3, 'smallpoints': 20, 'wins': 1, 'second_points': 0},
            {'games': 2, 'name': '3', 'points': 2, 'smallpoints': 15, 'wins': 0, 'second_points': 0},
            {'games': 1, 'name': '4', 'points': 1, 'smallpoints': 5, 'wins': 0, 'second_points': 0},
        ]

    def test_tie_situation(self):
        przyjaciele = 1
        kks_tg = 2
        kks_tg_junior = 3
        bekescaba = 4
        olimpia = 5
        self.mdrivers().games.list_for_group.return_value = [
            self._create_game(przyjaciele, 49, kks_tg, 45),
            self._create_game(kks_tg_junior, 50, bekescaba, 44),
            self._create_game(przyjaciele, 55, olimpia, 32),
            self._create_game(kks_tg, 74, kks_tg_junior, 41),
            self._create_game(bekescaba, 59, olimpia, 27),
            self._create_game(kks_tg_junior, 51, przyjaciele, 48),
            self._create_game(kks_tg, 70, olimpia, 38),
            self._create_game(bekescaba, 49, przyjaciele, 43),
            self._create_game(olimpia, 66, kks_tg_junior, 40),
            self._create_game(kks_tg, 77, bekescaba, 60),
        ]

        assert list(self.object().make_scores()) == [
            {
                'games': 4,
                'name': str(kks_tg),
                'points': 7,
                'smallpoints': 266,
                'wins': 3,
                'second_points': 0,
            },
            {
                'games': 4,
                'name': str(kks_tg_junior),
                'points': 6,
                'smallpoints': 182,
                'wins': 2,
                'second_points': 4,
            },
            {
                'games': 4,
                'name': str(bekescaba),
                'points': 6,
                'smallpoints': 212,
                'wins': 2,
                'second_points': 3,
            },
            {
                'games': 4,
                'name': str(przyjaciele),
                'points': 6,
                'smallpoints': 195,
                'wins': 2,
                'second_points': 2,
            },
            {
                'games': 4,
                'name': str(olimpia),
                'points': 5,
                'smallpoints': 163,
                'wins': 1,
                'second_points': 0,
            },
        ]

    def test_make(self):
        self.mmake_scores()
        self.object().context = {}

        self.object().make()

        assert self.object().context == {
            'teams': self.mmake_scores().return_value,
            'group': self.mgroup(),
        }


class TestLadderWidget(ScoreCase):

    @cache
    def object(self):
        obj = LadderWidget(self.mevent(), self.mgroup())
        obj.feed_request(self.mrequest())
        return obj

    @cache
    def mdumps(self):
        return self.patch('impex.groups.widgets.dumps')

    def test_data(self):
        self.mdumps()
        games = [
            self._create_game(1, 2, 2, 4),
            self._create_game(3, 8, 4, 16),
            self._create_game(1, 32, 4, 64),
            self._create_game(2, 128, 3, 256),
        ]
        games[3].is_ended = False
        self.mdrivers().games.list_for_group.return_value = games

        assert self.object().data() == self.mdumps().return_value
        self.mdumps().assert_called_once_with({
            'teams': [('1', '2'), ('3', '4')],
            'results': [
                [[2, 4], [8, 16]],
                [None, [32, 64]],
            ]
        })
