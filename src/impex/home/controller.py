from impex.application.controller import Controller


class HomeController(Controller):

    renderer = 'impex.home:templates/me.haml'
    permission = 'auth'
