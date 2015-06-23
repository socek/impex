from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:me.haml'

    def make(self):
        data = self.drivers.SampleData.find_all()
        self.database().commit()
        self.context['data'] = data
