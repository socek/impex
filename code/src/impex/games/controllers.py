from impex.application.controller import Controller
from impex.application.testing import cache

from impex.events.widgets import EventWidget
from impex.groups.widgets import GroupHighScoreWidget
from impex.groups.widgets import LadderWidget

from .widgets import GameWidget


class BaseGameList(Controller):

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


class GameListController(BaseGameList):

    renderer = 'impex.games:templates/list.haml'
    crumbs = 'games:list'

    def make(self):
        query = self._get_games()
        self.context['games'] = self._make_widgets(query)
        self.add_widget('event', EventWidget(self.event))

        if self.group_id:
            if self.group.ladder:
                self._on_ladder()
            else:
                self._on_highscore()
        else:
            self.context['highscore'] = None

    def _on_ladder(self):
        self.add_widget(
            'ladder',
            LadderWidget(
                self.event,
                self.group,
            ),
        )

    def _on_highscore(self):
        self.add_widget(
            'highscore',
            GroupHighScoreWidget(
                self.event,
                self.group,
            ),
        )

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


class GameShowController(BaseGameList):

    renderer = 'impex.games:templates/show.haml'
    crumbs = 'games:list'

    @property
    @cache
    def game_id(self):
        return self.matchdict['game_id']

    @property
    @cache
    def game(self):
        return self.drivers.games.get_by_id(self.game_id)

    def make(self):
        self.add_widget('event', EventWidget(self.event))
        self.add_widget('game', GameWidget(self.game))


class TimetableController(BaseGameList):

    renderer = 'impex.games:templates/timetable.haml'
    crumbs = 'games:list'

    def make(self):
        self.add_widget('event', EventWidget(self.event))
        self.context['games'] = self._get_games()

    def _get_games(self):
        return self.drivers.games.list(self.event_id)
