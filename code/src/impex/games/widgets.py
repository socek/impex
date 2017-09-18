from implugin.jinja2.widget import SingleWidget

from impex.application.plugins.formskit import FormWidget
from impex.application.requestable import Requestable

from .forms import CreateGameForm
from .forms import EditGameForm
from .forms import EditScoreGameForm


class CreateGameFormWidget(FormWidget):
    template = 'impex.games:templates/widgets/create_form.haml'
    form = CreateGameForm


class EditGameFormWidget(FormWidget):
    template = 'impex.games:templates/widgets/edit_form.haml'
    form = EditGameForm


class ScoreBoardWidget(FormWidget):
    template = 'impex.games:templates/widgets/scoreboard.haml'
    form = EditScoreGameForm


class GameWidget(SingleWidget, Requestable):
    template = 'impex.games:templates/widgets/game.haml'

    def __init__(self, game):
        self.game = game

    def make(self):
        self.context['game'] = self.game
        self.context['edit_url'] = self.route_path(
            'games:admin:edit_scores',
            event_id=self.matchdict['event_id'],
            game_id=self.game.id,
        )
