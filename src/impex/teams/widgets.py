from impex.application.plugins.formskit import FormWidget

from .forms import CreateTeamForm
from .forms import EditTeamForm


class CreateTeamFormWidget(FormWidget):
    template = 'impex.teams:templates/widgets/create_form.haml'
    form = CreateTeamForm


class EditTeamFormWidget(FormWidget):
    template = 'impex.teams:templates/widgets/edit_form.haml'
    form = EditTeamForm
