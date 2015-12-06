from datetime import datetime
from freezegun import freeze_time
from mock import MagicMock
from mock import sentinel

from ..forms import CreateGameForm
from ..forms import EditGameForm
from impex.application.testing import PostFormCase
from impex.application.testing import cache


class TestCreateEventForm(PostFormCase):
    _object_cls = CreateGameForm

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


class TestEditGameForm(PostFormCase):
    _object_cls = EditGameForm

    def test_on_success(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'plaing_at': sentinel.plaing_at,
            'priority': sentinel.priority,
            'left_id': sentinel.left_id,
            'right_id': sentinel.right_id,
        }
        self.minstance()

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        assert self.minstance().plaing_at == sentinel.plaing_at
        assert self.minstance().priority == sentinel.priority
        assert self.minstance().left_id == sentinel.left_id
        assert self.minstance().right_id == sentinel.right_id
        self.mdrivers().games.update.assert_called_once_with(
            self.minstance()
        )

    @freeze_time("2012-01-14 15:15")
    def test_read_from(self):
        instance = MagicMock()

        instance.plaing_at = datetime.now()
        instance.priority = 3
        instance.left_id = sentinel.left_id
        instance.right_id = sentinel.right_id

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'plaing_at': datetime.now(),
            'priority': 3,
            'left_id': sentinel.left_id,
            'right_id': sentinel.right_id,
        }

        assert self.object().instance is instance

    @cache
    def mpriorities(self):
        elements = []
        self.mdrivers().games.find_by_priority.return_value = elements

        for loop in range(5):
            obj = MagicMock()
            obj.priority = loop + 3
            elements.append(obj)
        return elements

    def test_fix_priorities_on_new_priority(self):
        del self.mpriorities()[:]
        self.matchdict()['event_id'] = sentinel.event_id

        self.object()._fix_priorities(sentinel.priority)
        self.mdrivers().games.find_by_priority.assert_called_once_with(
            sentinel.event_id,
            sentinel.priority,
        )

    def test_fix_priorities(self):
        self.mdrivers()
        elements = self.mpriorities()
        self.matchdict()['event_id'] = sentinel.event_id

        self.object()._fix_priorities(sentinel.priority)
        self.mdrivers().games.find_by_priority.assert_called_once_with(
            sentinel.event_id,
            sentinel.priority,
        )
        prorities = [element.priority for element in elements]
        assert prorities == [4, 5, 6, 7, 8]
        assert self.mdrivers().games.update.called
