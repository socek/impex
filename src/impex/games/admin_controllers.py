from impex.application.controller import Controller

from .widgets import CreateGameFormWidget
from .widgets import EditGameFormWidget
from .widgets import ScoreBoardWidget


class BaseController(Controller):

    def get_event(self):
        return self.drivers.events.get_by_id(self.matchdict['event_id'])


class GameListController(BaseController):

    renderer = 'impex.games:templates/admin/list.haml'
    permission = 'admin'
    crumbs = 'games:admin:list'

    def make(self):
        self.context['games'] = self.drivers.games.list(
            self.matchdict['event_id']
        )


class GameCreateController(BaseController):

    renderer = 'impex.games:templates/admin/create.haml'
    permission = 'admin'
    crumbs = 'games:admin:create'

    def make(self):
        form = self.add_form_widget(
            CreateGameFormWidget,
            event=self.get_event(),
        )
        form.fill()

        if form.validate():
            self.add_flashmsg('Dodano mecz.', 'info')
            self.redirect(
                'games:admin:list',
                event_id=self.matchdict['event_id'],
            )


class GameEditController(BaseController):

    renderer = 'impex.games:templates/admin/edit.haml'
    permission = 'admin'
    crumbs = 'games:admin:edit'

    def make(self):
        game_id = self.matchdict['game_id']
        game = self.drivers.games.get_by_id(game_id)
        form = self.add_form_widget(
            EditGameFormWidget,
            event=self.get_event(),
        )
        form.read_from(game)

        if form.validate():
            self.add_flashmsg('Zapisano zmiany w meczu.', 'info')
            self.redirect(
                'games:admin:list',
                event_id=self.matchdict['event_id'],
            )


class GameEditScoresController(BaseController):
    renderer = 'impex.games:templates/admin/edit_scores.haml'
    permission = 'admin'
    crumbs = 'games:admin:edit_scores'

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
