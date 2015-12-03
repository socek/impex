from impex.application.controller import Controller


class GameListController(Controller):

    renderer = 'impex.games:templates/admin/list.haml'
    permission = 'admin'

    def set_crumbs(self, widget):
        route = self.route_path('home')
        widget.add_breadcrumb('Główna', route)
        widget.add_breadcrumb('Panel Administracyjny', None, True)
        widget.add_breadcrumb('Wydarzenia', self.route_path('events:admin:list'))
        widget.add_breadcrumb('Mecze', None, True)

    def make(self):
        self.context['games'] = self.drivers.games.list(self.matchdict['event_id'])
