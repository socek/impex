from ..models import Group


class TestGroup(object):

    def test_init(self):
        assert Group().games_len() == 0
