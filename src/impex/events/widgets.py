from impex.application.plugins.formskit import FormWidget

from .forms import CreateEventForm
from .forms import EditEventForm


class CreateEventFormWidget(FormWidget):
    template = 'impex.events:templates/widgets/create_form.haml'
    form = CreateEventForm


class EditEventFormWidget(FormWidget):
    template = 'impex.events:templates/widgets/edit_form.haml'
    form = EditEventForm
