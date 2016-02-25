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


class ScoresTabWidget(BaseScoreTabWidget):
    name = 'scores'
    speed = 12
    template = 'impex.sliders:templates/widgets/scores.haml'

    def make(self):
        super().make()
        self.context['games'] = self._generate_games()

    def _generate_games(self):
        query = self.drivers.games.list(self.event_id)
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget

    def __call__(self, *args, **kwargs):
        self.make(*args, **kwargs)
        rer = self.render(self.get_template())
        return rer


class HighScoresTabWidget(BaseScoreTabWidget):
    name = 'high_scores'
    speed = 20
    template = 'impex.sliders:templates/widgets/high_scores.haml'

    def make(self):
        super().make()
        self.context['groups'] = []
        groups = self.drivers.groups.list_not_empty(self.event.id)
        for group in groups:
            self._append_group(group)

    def _append_group(self, group):
        widget_cls = LadderWidget if group.ladder else GroupHighScoreWidget
        widget = widget_cls(self.event, group)
        widget.feed_request(self.request)
        self.context['groups'].append(widget)
