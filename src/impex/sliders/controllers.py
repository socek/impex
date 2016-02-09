from impaf.controller.json import JsonController
from impex.application.controller import Controller
from impex.application.requestable import Requestable
from impex.application.testing import cache
from impex.games.widgets import GameWidget

from .widgets import FirstTabWidget
from .widgets import ScoresTabWidget
# from .widgets import SecondTabWidget


class TabsController(object):

    def make_tabs(self):
        self.tabs = {}
        self.add_tab(FirstTabWidget)
        # self.add_tab(SecondTabWidget)
        self.add_tab(ScoresTabWidget)
        return self.tabs

    def add_tab(self, cls, *args, **kwargs):
        tab = cls(*args, **kwargs)
        tab.feed_request(self.request)
        self.tabs[tab.name] = tab


class SliderShowController(Controller, TabsController):

    renderer = 'impex.sliders:templates/show.haml'

    @property
    @cache
    def event_id(self):
        return self.matchdict['event_id']

    @property
    @cache
    def event(self):
        return self.drivers.events.get_by_id(self.event_id)

    def make(self):
        self.context['tabs'] = self.make_tabs()

    def _make_widgets(self, query):
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget


class SliderCommand(JsonController, Requestable, TabsController):

    def make(self):
        tabs = list(self.make_tabs().values())
        number = self.session.get('number', 0)
        try:
            self.context = tabs[number].to_dict()
        except IndexError:
            number = 0
            self.context = tabs[number].to_dict()
        self.session['number'] = number + 1
        self.session.save()
