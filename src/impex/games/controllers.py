from impex.application.controller import Controller
from impex.application.testing import cache

from impex.groups.widgets import GroupHighScoreWidget
from impex.groups.widgets import LadderWidget
from impex.events.widgets import EventWidget

from .widgets import GameWidget


class GameListController(Controller):

    renderer = 'impex.games:templates/list.haml'
    crumbs = 'games:list'

    @property
    @cache
    def group_id(self):
        return self.matchdict.get('group_id', None)

    @property
    @cache
    def event_id(self):
        return self.matchdict['event_id']

    @property
    @cache
    def group(self):
        return self.drivers.groups.get_by_id(self.group_id)

    @property
    @cache
    def event(self):
        return self.drivers.events.get_by_id(self.event_id)

    def make(self):
        query = self._get_games()
        self.context['games'] = self._make_widgets(query)
        self.add_widget('event', EventWidget(self.event))

        if self.group_id:
            if self.group.ladder:
                self.add_widget(
                    'ladder',
                    LadderWidget(
                        self.event,
                        self.group,
                    ),
                )
            else:
                self.add_widget(
                    'highscore',
                    GroupHighScoreWidget(
                        self.event,
                        self.group,
                    ),
                )
        else:
            self.context['highscore'] = None

    def _make_widgets(self, query):
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget

    def _get_games(self):
        if self.group_id:
            return self.drivers.games.list_for_group(self.event_id, self.group_id)
        else:
            return self.drivers.games.list(self.event_id)
