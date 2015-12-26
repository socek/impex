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
