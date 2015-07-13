from pyramid.security import remember

from impex.application.controller import Controller
from .forms import FirstForm


class HomeController(Controller):

    renderer = 'impex.home:templates/me.haml'
    permission = 'auth_view'

    def make(self):
        data = self.drivers.SampleData.find_all()
        self.context['data'] = data
        form = self.add_form(FirstForm)
        if form.validate():
            self.add_flashmsg('info', 'success')
            self.redirect('home')


class LoginController(Controller):

    def make(self):
        user = self.drivers.Auth.find_all().first()
        self.redirect('home')
        headers = remember(self.request, str(user.id))
        self.response.headers.extend(headers)
