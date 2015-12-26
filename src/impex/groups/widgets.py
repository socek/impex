from impex.application.plugins.formskit import FormWidget

from .forms import CreateGroupForm
from .forms import EditGroupForm


class CreateGroupFormWidget(FormWidget):
    template = 'impex.groups:templates/widgets/create_form.haml'
    form = CreateGroupForm


class EditGroupFormWidget(FormWidget):
    template = 'impex.groups:templates/widgets/edit_form.haml'
    form = EditGroupForm
