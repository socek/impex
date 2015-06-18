from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:me.haml'

    def make(self):
        print('start')
        self.database()
        self.database()
