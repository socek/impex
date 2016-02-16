from .base import TabWidget
from impex.application.testing import cache
from impex.games.widgets import GameWidget


class ScoresTabWidget(TabWidget):
    name = 'scores'
    speed = 12
    template = 'impex.sliders:templates/widgets/scores.haml'

    @property
    @cache
    def event_id(self):
        return self.matchdict['event_id']

    @property
    @cache
    def event(self):
        return self.drivers.events.get_by_id(self.event_id)

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
