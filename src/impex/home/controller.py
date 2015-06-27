from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:templates/me.haml'

    def make(self):
        data = self.drivers.SampleData.find_all()
        self.context['data'] = data
