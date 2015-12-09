from formskit.converters import ToDatetime
from formskit.converters import ToInt
from formskit.formvalidators import FormValidator
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


class GameValidator(FormValidator):
    message = 'That game already exists in this event!'

    def validate(self):
        left_id = self.form.get_value('left_id')
        right_id = self.form.get_value('right_id')
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
        return left_id != right_id


class CreateGameForm(PostForm):

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

        self.add_form_validator(GameValidator())
        self.add_form_validator(TeamsMustDifferValidator())

    def fill(self):
        self.set_value(
            'priority',
            self.drivers.games.get_next_avalible_priority(
                int(self.matchdict['event_id'])
            )
        )

    def _get_teams(self):
        return self.drivers.teams.list()

    def on_success(self):
        data = self.get_data_dict(True)

        game = self.drivers.games.create(
            plaing_at=data['plaing_at'],
            priority=data['priority'],
            left_id=data['left_id'],
            right_id=data['right_id'],
            event_id=self.matchdict['event_id'],
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

        self.instance.plaing_at = data['plaing_at']
        self.instance.priority = data['priority']
        self.instance.left_id = data['left_id']
        self.instance.right_id = data['right_id']
        self.drivers.games.update(self.instance)
        self.database().commit()
        self._fix_priorities(data['priority'], self.instance)

    def read_from(self, game):
        self.set_value('plaing_at', game.plaing_at)
        self.set_value('priority', game.priority)
        self.set_value('left_id', str(game.left_id))
        self.set_value('right_id', str(game.right_id))
        self.instance = game
