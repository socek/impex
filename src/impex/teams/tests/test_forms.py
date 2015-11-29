from mock import sentinel

from ..forms import CreateTeamForm
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
