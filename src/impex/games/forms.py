from collections import namedtuple

from formskit.converters import ToDatetime
from formskit.converters import ToInt
from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm

Status = namedtuple('status', ['id', 'name'])
Game = namedtuple('game', ['id', 'name'])
Team = namedtuple('team', ['id', 'name'])
Place = namedtuple('place', ['id', 'name'])


class GameValidator(FormValidator):
    message = 'That game already exists in this event!'

    def validate(self):
        left_id = self.form.get_value('left_id')
        left_id = left_id if left_id else None
        right_id = self.form.get_value('right_id')
        right_id = right_id if right_id else None
        if getattr(self.form, 'instance', None):
            except_id = self.form.instance.id
        else:
            except_id = None

        return not self.form.drivers.games.is_doubled(
            self.form.matchdict['event_id'],
            left_id,
            right_id,
            except_id,
        )


class TeamsMustDifferValidator(FormValidator):
    message = 'Teams can not be the same.'

    def validate(self):
        left_id = self.form.get_value('left_id')
        right_id = self.form.get_value('right_id')
        return left_id == '' or right_id == '' or left_id != right_id


class CreateGameForm(PostForm):

    def __init__(self, *args, event=None, **kwargs):
        super().__init__(*args, **kwargs)
        self.event = event

    def create_form(self):
        self.add_field(
            'plaing_at',
            label='Kiedy',
            convert=ToDatetime(),
        )

        self.add_field(
            'priority',
            label='Prioryter',
            validators=[NotEmpty()],
            convert=ToInt(),
        )

        self.add_field(
            'left_id',
            label='Pierwsza drużyna',
        ).set_avalible_values(self._get_teams)

        self.add_field(
            'right_id',
            label='Druga drużyna',
        ).set_avalible_values(self._get_teams)
        self.add_field(
            'group_id',
            label='Grupa',
        ).set_avalible_values(self._get_groups)
        self.add_field(
            'child_id',
            label='Następny mecz',
        ).set_avalible_values(self._get_games)
        self.add_field(
            'place_id',
            label='Miejsce',
        ).set_avalible_values(self._get_places)

        self.add_form_validator(GameValidator())
        self.add_form_validator(TeamsMustDifferValidator())

    def fill(self):
        event = self.drivers.events.get_by_id(self.matchdict['event_id'])
        self.set_value(
            'plaing_at',
            event.start_date,
        )
        self.set_value(
            'priority',
            self.drivers.games.get_next_avalible_priority(
                int(self.matchdict['event_id'])
            )
        )

    def _get_teams(self):
        yield Team(id='', name='(brak)')
        for team in self.drivers.teams.list():
            yield team

    def _get_groups(self):
        return self.drivers.groups.list()

    def _get_places(self):
        yield Place(id='', name='(brak)')
        for place in self.drivers.places.list():
            yield place

    def _get_games(self):
        if getattr(self, 'instance', None):
            query = self.drivers.games.list_except(
                self.event.id,
                self.instance.id,
                self.instance.group_id,
            )
        else:
            query = self.drivers.games.list(self.event.id)
        yield Game(id='', name='(brak)')
        for game in query:
            name = '%d: %s %s' % (
                game.priority,
                getattr(game.left, 'name', ''),
                getattr(game.right, 'name', ''),
            )
            yield Game(id=game.id, name=name)

    def on_success(self):
        data = self.get_data_dict(True)

        left_id = data['left_id'] if data['left_id'] else None
        right_id = data['right_id'] if data['right_id'] else None
        child_id = data['child_id'] if data['child_id'] else None
        place_id = data['place_id'] if data['place_id'] else None

        game = self.drivers.games.create(
            plaing_at=data['plaing_at'],
            priority=data['priority'],
            group_id=data['group_id'],
            left_id=left_id,
            right_id=right_id,
            event_id=self.matchdict['event_id'],
            child_id=child_id,
            place_id=place_id,
        )
        self.database().commit()
        self._fix_priorities(data['priority'], game)

    def _fix_priorities(self, priority, game):
        self.drivers.games.increment_priorities_by(
            self.matchdict['event_id'],
            priority,
            game,
        )
        self.database().commit()


class EditGameForm(CreateGameForm):

    def on_success(self):
        data = self.get_data_dict(True)

        left_id = data['left_id'] if data['left_id'] else None
        right_id = data['right_id'] if data['right_id'] else None
        child_id = data['child_id'] if data['child_id'] else None
        place_id = data['place_id'] if data['place_id'] else None

        self.instance.plaing_at = data['plaing_at']
        self.instance.priority = data['priority']
        self.instance.left_id = left_id
        self.instance.right_id = right_id
        self.instance.child_id = child_id
        self.instance.group_id = data['group_id']
        self.instance.place_id = place_id
        self.drivers.games.update(self.instance)
        self.database().commit()
        self._fix_priorities(data['priority'], self.instance)

    def read_from(self, game):
        self.set_value('plaing_at', game.plaing_at)
        self.set_value('priority', game.priority)
        self.set_value('left_id', str(game.left_id))
        self.set_value('right_id', str(game.right_id))
        self.set_value('group_id', str(game.group_id))
        self.set_value('child_id', str(game.child_id))
        self.set_value('place_id', str(game.place_id))
        self.instance = game


class EditScoreGameForm(PostForm):

    def read_from(self, game):
        self.instance = game
        self.left = game.left
        self.right = game.right

        for team, scores in self.instance.scores.items():
            for index, quart in enumerate(scores):
                key = '%s_quart_%d' % (
                    team,
                    index + 1,
                )
                self.set_value(key, quart)

        self.set_value('status', self.instance.status)

    def _get_statuses(self):
        for key, value in self.instance.STATUSES.items():
            yield Status(id=key, name=value)

    def _quarts(self):
        for team in ['left', 'right']:
            for quart in range(4):
                yield team, quart + 1, '%s_quart_%d' % (team, quart + 1),

    def create_form(self):
        for _, _, key in self._quarts():
            self.add_field(
                key,
                convert=ToInt(),
            )
            self.add_field(
                key + '_sum',
            )

        self.add_field(
            'status',
            label='Status',
            convert=ToInt(),
        ).set_avalible_values(self._get_statuses)

    def on_success(self):
        data = self.get_data_dict(True)
        self.instance.status = data['status']
        self.instance.scores = {'left': [], 'right': []}
        for team, quart, key in self._quarts():
            if data[key]:
                self.instance.scores[team].append(data[key])
            else:
                self.instance.scores[team].append(0)

        self.drivers.games.update(self.instance)
        self.database().commit()
