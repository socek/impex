from mock import sentinel

from impaf.testing import cache

from ..forms import CreateGameForm
from impex.application.testing import PostFormCase


class TestCreateEventForm(PostFormCase):
    _object_cls = CreateGameForm

    @cache
    def mset_value(self):
        return self.pobject(self.object(), 'set_value')

    def test_on_success(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'plaing_at': sentinel.plaing_at,
            'priority': sentinel.priority,
            'left_id': sentinel.left_id,
            'right_id': sentinel.right_id,
        }
        self.matchdict()['event_id'] = sentinel.event_id

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        self.mdrivers().games.create.assert_called_once_with(
            plaing_at=sentinel.plaing_at,
            priority=sentinel.priority,
            left_id=sentinel.left_id,
            right_id=sentinel.right_id,
            event_id=sentinel.event_id,
        )
        self.mdatabase().commit.assert_called_once_with()

    def test_fill(self):
        self.mdrivers()
        self.mset_value()
        self.matchdict()['event_id'] = '3'

        self.object().fill()

        self.mset_value().assert_called_once_with(
            'priority',
            self.mdrivers().games.get_next_avalible_priority.return_value,
        )
        self.mdrivers().games.get_next_avalible_priority.assert_called_once_with(
            3
        )

    def test_get_teams(self):
        self.mdrivers()

        assert self.object()._get_teams() == self.mdrivers().teams.list.return_value
