from impex.application.controller import Controller

from .widgets import SliderAdminFormWidget


class SliderAdminController(Controller):

    renderer = 'impex.sliders:templates/admin/show.haml'

    def make(self):
        form = self.add_form_widget(
            SliderAdminFormWidget,
        )
        if form.validate():
            self.add_flashmsg('Zapisano.', 'info')
