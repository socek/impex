from impex.application.controller import Controller

from .widgets import CreateGameFormWidget


class GameListController(Controller):

    renderer = 'impex.games:templates/admin/list.haml'
    permission = 'admin'

    def set_crumbs(self, widget):
        route = self.route_path('home')
        widget.add_breadcrumb('Główna', route)
        widget.add_breadcrumb('Panel Administracyjny', None, True)
        widget.add_breadcrumb(
            'Wydarzenia', self.route_path('events:admin:list'))
        widget.add_breadcrumb('Mecze', None, True)

    def make(self):
        self.context['games'] = self.drivers.games.list(
            self.matchdict['event_id'])


class GameCreateController(Controller):

    renderer = 'impex.games:templates/admin/create.haml'
    permission = 'admin'

    def set_crumbs(self, widget):
        route = self.route_path('home')
        widget.add_breadcrumb('Główna', route)
        widget.add_breadcrumb('Panel Administracyjny', None, True)
        widget.add_breadcrumb(
            'Wydarzenia', self.route_path('events:admin:list'))
        widget.add_breadcrumb(
            'Mecze',
            self.route_path(
                'games:admin:list',
                event_id=self.matchdict['event_id'],
            ),
        )
        widget.add_breadcrumb('Dodawanie', None, True)

    def make(self):
        form = self.add_form_widget(CreateGameFormWidget)
        form.fill()

        if form.validate():
            self.add_flashmsg('Dodano mecz.', 'info')
            self.redirect(
                'games:admin:list',
                event_id=self.matchdict['event_id'],
            )
