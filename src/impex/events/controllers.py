from impex.application.controller import Controller

from .widgets import EventWidget


class EventListController(Controller):

    renderer = 'impex.events:templates/list.haml'
    crumbs = 'home'

    def make(self):
        self.context['events'] = self._make_widgets(self.drivers.events.list_for_user())

    def _make_widgets(self, query):
        for game in query:
            widget = EventWidget(game)
            widget.feed_request(self.request)
            yield widget
