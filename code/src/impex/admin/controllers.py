from impex.application.controller import Controller


class AdminController(Controller):

    renderer = 'impex.admin:templates/home.haml'
    permission = 'admin'
    crumbs = 'admin:home'
