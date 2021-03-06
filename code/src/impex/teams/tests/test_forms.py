from mock import MagicMock
from mock import sentinel

from impaf.testing import cache

from ..forms import CreateTeamForm
from ..forms import EditTeamForm
from impex.application.testing import PostFormCase


class TestCreateTeamForm(PostFormCase):
    _object_cls = CreateTeamForm

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'name': sentinel.name,
            'hometown': sentinel.hometown,
        }

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().teams.create.assert_called_once_with(
            name=sentinel.name,
            hometown=sentinel.hometown,
        )
        self.mdatabase().commit.assert_called_once_with()


class TestEditTeamForm(PostFormCase):
    _object_cls = EditTeamForm

    @cache
    def minstance(self):
        self.object().instance = MagicMock()
        return self.object().instance

    def test_make(self):
        self.mdatabase()
        self.mdrivers()
        self.minstance()
        self.mdata().return_value = {
            'name': sentinel.name,
            'hometown': sentinel.hometown,
        }

        self.object().on_success()

        assert self.minstance().name == sentinel.name
        assert self.minstance().hometown == sentinel.hometown
        self.mdrivers().teams.update.assert_called_once_with(
            self.minstance()
        )

    def test_read_from(self):
        instance = MagicMock()
        instance.name = sentinel.name
        instance.hometown = sentinel.hometown

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'hometown': sentinel.hometown,
            'name': sentinel.name,
        }

        assert self.object().instance is instance
