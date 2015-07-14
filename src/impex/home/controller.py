from impex.application.controller import Controller

from .forms import FirstForm


class HomeController(Controller):

    renderer = 'impex.home:templates/me.haml'
    permission = 'auth'

    def make(self):
        data = self.drivers.SampleData.find_all()
        self.context['data'] = data
        form = self.add_form(FirstForm)
        if form.validate():
            self.add_flashmsg('info', 'success')
            self.redirect('home')
