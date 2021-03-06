from datetime import datetime
from freezegun import freeze_time
from mock import MagicMock
from mock import call
from mock import sentinel

from impex.application.testing import PostFormCase
from impex.application.testing import ValidatorCase
from impex.application.testing import cache

from ..forms import CreateGameForm
from ..forms import EditGameForm
from ..forms import EditScoreGameForm
from ..forms import GameValidator
from ..forms import TeamsMustDifferValidator


class TestCreateGameForm(PostFormCase):
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
            'group_id': sentinel.group_id,
            'child_id': sentinel.child_id,
            'place_id': sentinel.place_id,
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
            group_id=sentinel.group_id,
            child_id=sentinel.child_id,
            place_id=sentinel.place_id,
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

        assert self.mset_value().call_args_list == [
            call(
                'plaing_at',
                self.mdrivers().events.get_by_id.return_value.start_date,
            ),
            call(
                'priority',
                self.mdrivers().games.get_next_avalible_priority.return_value,
            )
        ]
        self.mdrivers().games.get_next_avalible_priority.assert_called_once_with(
            3
        )

    def test_get_teams(self):
        team = MagicMock()
        self.mdrivers().teams.list.return_value = [team]

        data = list(self.object()._get_teams())
        assert data[0].id == ''
        assert data[0].name == '(brak)'
        assert data[1].id == team.id
        assert data[1].name == team.name

    def test_get_places(self):
        place = MagicMock()
        self.mdrivers().places.list.return_value = [place]

        data = list(self.object()._get_places())
        assert data[0].id == ''
        assert data[0].name == '(brak)'
        assert data[1].id == place.id
        assert data[1].name == place.name

    def test_get_groups(self):
        self.mdrivers()

        assert self.object()._get_groups() == self.mdrivers().groups.list.return_value

    def test_get_games(self):
        game = MagicMock()
        game.priority = 1
        game.left.name = 'myname'
        game.right = None
        self.mdrivers().games.list.return_value = [game]
        self.object().event = MagicMock()

        data = list(self.object()._get_games())
        assert data[0].id == ''
        assert data[0].name == '(brak)'
        assert data[1].id == game.id
        assert data[1].name == '1: myname '

    def test_get_games_with_instance(self):
        game = MagicMock()
        game.priority = 1
        game.left.name = 'myname'
        game.right = None
        instance = MagicMock()
        event = MagicMock()
        self.mdrivers().games.list_except.return_value = [game]
        self.object().event = event
        self.object().instance = instance

        data = list(self.object()._get_games())
        assert data[0].id == ''
        assert data[0].name == '(brak)'
        assert data[1].id == game.id
        assert data[1].name == '1: myname '

        self.mdrivers().games.list_except.assert_called_once_with(
            event.id,
            instance.id,
            instance.group_id,
        )


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
            'group_id': sentinel.group_id,
            'child_id': sentinel.child_id,
            'place_id': sentinel.place_id,
        }
        self.minstance()

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        assert self.minstance().plaing_at == sentinel.plaing_at
        assert self.minstance().priority == sentinel.priority
        assert self.minstance().left_id == sentinel.left_id
        assert self.minstance().right_id == sentinel.right_id
        assert self.minstance().group_id == sentinel.group_id
        assert self.minstance().child_id == sentinel.child_id
        assert self.minstance().place_id == sentinel.place_id
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
        instance.group_id = sentinel.group_id
        instance.child_id = sentinel.child_id
        instance.place_id = sentinel.place_id

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'plaing_at': datetime.now(),
            'priority': 3,
            'left_id': str(sentinel.left_id),
            'right_id': str(sentinel.right_id),
            'group_id': str(sentinel.group_id),
            'child_id': str(sentinel.child_id),
            'place_id': str(sentinel.place_id),
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


class TestGameValidator(ValidatorCase):
    _object_cls = GameValidator

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


class TestTeamsMustDifferValidator(ValidatorCase):
    _object_cls = TeamsMustDifferValidator

    def test_positive(self):
        def get_value_mock(name):
            if name == 'left_id':
                return sentinel.left_id
            else:
                return sentinel.right_id
        self.mform().get_value = get_value_mock
        assert self.object().validate() is True

    def test_negative(self):
        assert self.object().validate() is False

    def test_when_left_is_empty(self):
        def get_value_mock(name):
            if name == 'left_id':
                return ''
            else:
                return sentinel.right_id
        self.mform().get_value = get_value_mock
        assert self.object().validate() is True

    def test_when_right_is_empty(self):
        def get_value_mock(name):
            if name == 'left_id':
                return sentinel.left_id
            else:
                return ''
        self.mform().get_value = get_value_mock
        assert self.object().validate() is True


class TestEditScoreGameForm(PostFormCase):
    _object_cls = EditScoreGameForm

    def test_on_success(self):
        self.mdatabase()
        self.mdrivers()
        self.mdata().return_value = {
            'status': 2,
            'left_quart_1': 5,
            'left_quart_2': 10,
            'left_quart_3': 15,
            'left_quart_4': 0,
            'right_quart_1': 10,
            'right_quart_2': 15,
            'right_quart_3': 20,
            'right_quart_4': '',
        }
        self.minstance()

        self.object().on_success()

        self.mdata().assert_called_once_with(True)
        assert self.minstance().status == 2
        assert self.minstance().scores == {
            'left': [5, 10, 15, 0],
            'right': [10, 15, 20, 0],
        }
        self.mdrivers().games.update.assert_called_once_with(
            self.minstance()
        )

    def test_read_from(self):
        instance = MagicMock()

        instance.status = 1
        instance.scores = {
            'left': [5, 10, 15, 20],
            'right': [10, 15, 20, 25],
        }

        self.object().read_from(instance)

        assert self.object().get_data_dict(True) == {
            'csrf_token': self.mget_csrf_token().return_value,
            'status': 1,
            'left_quart_1': 5,
            'left_quart_2': 10,
            'left_quart_3': 15,
            'left_quart_4': 20,
            'right_quart_1': 10,
            'right_quart_2': 15,
            'right_quart_3': 20,
            'right_quart_4': 25,
        }

        assert self.object().instance is instance

    def test_get_statuses(self):
        self.minstance().STATUSES = {0: 'something'}
        data = list(self.object()._get_statuses())
        assert data[0].id == 0
        assert data[0].name == 'something'
