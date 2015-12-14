from impex.application.controller import Controller

from .widgets import CreateGameFormWidget
from .widgets import EditGameFormWidget
from .widgets import ScoreBoardWidget


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


class GameEditController(Controller):

    renderer = 'impex.games:templates/admin/edit.haml'
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
        widget.add_breadcrumb('Edycja', None, True)

    def make(self):
        game_id = self.matchdict['game_id']
        game = self.drivers.games.get_by_id(game_id)
        form = self.add_form_widget(EditGameFormWidget)
        form.read_from(game)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w meczu.', 'info')
            self.redirect(
                'games:admin:list',
                event_id=self.matchdict['event_id'],
            )


class GameEditScoresController(Controller):
    renderer = 'impex.games:templates/admin/edit_scores.haml'
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
        widget.add_breadcrumb('Tabela wyników', None, True)

    def make(self):
        game_id = self.matchdict['game_id']
        game = self.drivers.games.get_by_id(game_id)
        form = self.add_form_widget(ScoreBoardWidget)
        form.read_from(game)

        if form.validate():
            self.add_flashmsg('Zapisano tabelę wyników.', 'info')
            self.redirect(
                'games:admin:edit_scores',
                event_id=self.matchdict['event_id'],
                game_id=self.matchdict['game_id'],
            )
