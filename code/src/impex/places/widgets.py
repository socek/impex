from impex.application.plugins.formskit import FormWidget

from .forms import CreatePlaceForm
from .forms import EditPlaceForm


class CreatePlaceFormWidget(FormWidget):
    template = 'impex.places:templates/widgets/create_form.haml'
    form = CreatePlaceForm


class EditPlaceFormWidget(FormWidget):
    template = 'impex.places:templates/widgets/edit_form.haml'
    form = EditPlaceForm
