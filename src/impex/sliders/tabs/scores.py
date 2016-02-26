from .base import TabWidget
from impex.application.testing import cache
from impex.games.widgets import GameWidget
from impex.groups.widgets import GroupHighScoreWidget
from impex.groups.widgets import LadderWidget


class BaseScoreTabWidget(TabWidget):

    @property
    @cache
    def event_id(self):
        return self.matchdict['event_id']

    @property
    @cache
    def event(self):
        return self.drivers.events.get_by_id(self.event_id)

    def _generate_games(self, query):
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget


class ScoresTabWidget(BaseScoreTabWidget):
    name = 'scores'
    speed = 12
    template = 'impex.sliders:templates/widgets/scores.haml'

    def make(self):
        super().make()
        query = self.drivers.games.list(self.event_id)
        self.context['games'] = self._generate_games(query)

    def __call__(self, *args, **kwargs):
        self.make(*args, **kwargs)
        rer = self.render(self.get_template())
        return rer


class HighScoresTabWidget(BaseScoreTabWidget):
    name = 'high_scores'
    speed = 20
    template = 'impex.sliders:templates/widgets/high_scores.haml'
    index = 0

    def make(self):
        super().make()
        self.context['groups'] = []
        self.groups = []
        groups = self.drivers.groups.list_not_empty(self.event.id)
        group = groups[self.index]
        self._append_group(group)

    def _append_group(self, group):
        widget_cls = LadderWidget if group.ladder else GroupHighScoreWidget
        widget = widget_cls(self.event, group)
        widget.feed_request(self.request)
        self.context['groups'].append(widget)
        self.groups.append(group)


class GroupATabWidget(HighScoresTabWidget):
    name = 'group_a'
    index = 0


class GroupBTabWidget(HighScoresTabWidget):
    name = 'group_b'
    index = 1


class FinalsTabWidget(HighScoresTabWidget):
    name = 'finals'
    index = 2

    def make(self):
        super().make()
        group = self.groups[0]
        query = self.drivers.games.list_for_group(self.event_id, group.id)
        self.context['games'] = self._generate_games(query)
