from impex.application.testing import DriverCase
from impex.groups.driver import GroupDriver
from impex.groups.models import Group
from impex.games.models import Game


class TestDriverGroup(DriverCase):
    _object_cls = GroupDriver

    def test_list(self):
        self.flush_table_from_object(Game, Group)
        self.object().create(name='one')
        self.object().create(name='two')
        self.object().create(name='three')
        self.object().create(name='four')
        self.database().commit()

        data = [obj.name for obj in self.object().list()]

        assert data == ['one', 'two', 'three', 'four']
