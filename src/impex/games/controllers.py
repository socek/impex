from impex.application.controller import Controller

from .widgets import GameWidget


class GameListController(Controller):

    renderer = 'impex.games:templates/list.haml'
    crumbs = 'games:list'

    def make(self):
        self.context['games'] = self._get_games()

    def _get_games(self):
        query = self.drivers.games.list(self.matchdict['event_id'])
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget
