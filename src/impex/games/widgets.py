from impex.application.plugins.formskit import FormWidget

from .forms import CreateGameForm
from .forms import EditGameForm


class CreateGameFormWidget(FormWidget):
    template = 'impex.games:templates/widgets/create_form.haml'
    form = CreateGameForm


class EditGameFormWidget(FormWidget):
    template = 'impex.games:templates/widgets/edit_form.haml'
    form = EditGameForm
