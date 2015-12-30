from impex.application.controller import Controller

from .widgets import GameWidget


class GameListController(Controller):

    renderer = 'impex.games:templates/list.haml'
    crumbs = 'games:list'

    def make(self):
        query = self._get_games()
        self.context['games'] = self._make_widgets(query)

    def _make_widgets(self, query):
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget

    def _get_games(self):
        event_id = self.matchdict['event_id']
        group_id = self.matchdict.get('group_id', None)
        if group_id:
            return self.drivers.games.list_for_group(event_id, group_id)
        else:
            return self.drivers.games.list(event_id)
