from impex.application.plugins.formskit import FormWidget

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
