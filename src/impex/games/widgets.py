from impex.application.plugins.formskit import FormWidget

from .forms import CreateGameForm


class CreateGameFormWidget(FormWidget):
    template = 'impex.games:templates/widgets/create_form.haml'
    form = CreateGameForm
