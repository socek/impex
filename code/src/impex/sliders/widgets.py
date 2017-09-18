from impex.application.plugins.formskit import FormWidget

from .forms import SliderAdminForm


class SliderAdminFormWidget(FormWidget):
    template = 'impex.sliders:templates/widgets/create_form.haml'
    form = SliderAdminForm
