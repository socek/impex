from datetime import datetime
from freezegun import freeze_time
from mock import MagicMock
from mock import sentinel

from ..forms import CreateGameForm
from ..forms import EditGameForm
from ..forms import GameValidator
from impex.application.testing import PostFormCase
from impex.application.testing import RequestCase
from impex.application.testing import cache


class TestCreateEventForm(PostFormCase):
    _object_cls = CreateGameForm

    @cache
    def mfix_fix_priorities(self):
        return self.pobject(self.object(), '_fix_priorities')

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
        self.mfix_fix_priorities()

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
        self.mfix_fix_priorities().assert_called_once_with(
            sentinel.priority,
            self.mdrivers().games.create.return_value,
        )

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
            'left_id': str(sentinel.left_id),
            'right_id': str(sentinel.right_id),
        }

        assert self.object().instance is instance

    def test_fix_priorities(self):
        self.mdrivers()
        self.matchdict()['event_id'] = sentinel.event_id
        self.mdatabase()

        self.object()._fix_priorities(sentinel.priority, sentinel.game)
        self.mdrivers().games.increment_priorities_by.assert_called_once_with(
            sentinel.event_id,
            sentinel.priority,
            sentinel.game,
        )
        self.mdatabase().commit.assert_called_once_with()


class TestGameValidator(RequestCase):

    @cache
    def mform(self):
        return MagicMock()

    @cache
    def object(self):
        validator = GameValidator()
        validator.set_form(self.mform())
        return validator

    def test_when_instance_is_present(self):
        self.mform().drivers.games.is_doubled.return_value = False
        self.mform().matchdict = {'event_id': sentinel.event_id}
        assert self.object().validate() is True
        self.mform().drivers.games.is_doubled.assert_called_once_with(
            sentinel.event_id,
            self.mform().get_value.return_value,
            self.mform().get_value.return_value,
            self.mform().instance.id,
        )

    def test_when_instance_is_not_present(self):
        self.mform().drivers.games.is_doubled.return_value = True
        self.mform().matchdict = {'event_id': sentinel.event_id}
        self.mform().instance = None
        assert self.object().validate() is False
        self.mform().drivers.games.is_doubled.assert_called_once_with(
            sentinel.event_id,
            self.mform().get_value.return_value,
            self.mform().get_value.return_value,
            None,
        )
