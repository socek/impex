from impex.application.testing import DriverCase
from impex.teams.driver import TeamDriver
from impex.teams.models import Team


class TestTeamDriver(DriverCase):
    _object_cls = TeamDriver

    def test_list(self):
        self.flush_table_from_object(Team)
        self.object().create(name='one')
        self.object().create(name='two')
        self.object().create(name='three')
        self.object().create(name='four')
        self.database().commit()

        data = [obj.name for obj in self.object().list()]

        assert data == ['four', 'one', 'three', 'two']
