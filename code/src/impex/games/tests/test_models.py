from ..models import Game


class TestGame(object):

    def test_get_sum_for_quart(self):
        game = Game()
        game.scores = {
            'left': [5, 10, 15, 20],
            'right': [5, 10, 20, 40],
        }

        assert game.get_sum_for_quart('left', 1) == 5
        assert game.get_sum_for_quart('left', 2) == 15
        assert game.get_sum_for_quart('left', 3) == 30
        assert game.get_sum_for_quart('left', 4) == 50
        assert game.get_sum_for_quart('right', 1) == 5
        assert game.get_sum_for_quart('right', 2) == 15
        assert game.get_sum_for_quart('right', 3) == 35
        assert game.get_sum_for_quart('right', 4) == 75

    def test_is_not_started(self):
        game = Game()
        game.status = game.STATUS_NOT_STARTED

        assert game.is_not_started is True
        assert game.is_running is False
        assert game.is_ended is False

    def test_is_running(self):
        game = Game()
        game.status = game.STATUS_RUNNING

        assert game.is_not_started is False
        assert game.is_running is True
        assert game.is_ended is False

    def test_is_ended(self):
        game = Game()
        game.status = game.STATUS_ENDED

        assert game.is_not_started is False
        assert game.is_running is False
        assert game.is_ended is True
