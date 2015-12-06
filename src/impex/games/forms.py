from formskit.converters import ToDatetime
from formskit.converters import ToInt
from formskit.validators import NotEmpty

from impex.application.plugins.formskit import PostForm


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

        self.drivers.games.create(
            plaing_at=data['plaing_at'],
            priority=data['priority'],
            left_id=data['left_id'],
            right_id=data['right_id'],
            event_id=self.matchdict['event_id'],
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

    def read_from(self, game):
        self.set_value('plaing_at', game.plaing_at)
        self.set_value('priority', game.priority)
        self.set_value('left_id', game.left_id)
        self.set_value('right_id', game.right_id)
        self.instance = game
