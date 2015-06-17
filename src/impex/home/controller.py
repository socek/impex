from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:me.haml'

    def make(self):
        print(self.session)
