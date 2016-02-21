from datetime import datetime
from time import mktime

from pyramid.response import Response

from impaf.controller.json import JsonController
from impex.application.controller import Controller
from impex.application.requestable import Requestable
from impex.application.testing import cache
from impex.games.widgets import GameWidget

from .tabs import TabList
from .events import RefreshEvent


class TabsController(object):

    @property
    @cache
    def tabs(self):
        return TabList(self.request).tabs

    @property
    def timestamp(self):
        return '%d' % (
            mktime(datetime.now().timetuple()),
        )


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
        self.context['tabs'] = self.tabs
        self.context['timestamp'] = self.timestamp
        self.context['event_id'] = self.event_id

    def _make_widgets(self, query):
        for game in query:
            widget = GameWidget(game)
            widget.feed_request(self.request)
            yield widget


class SliderCommand(JsonController, Requestable, TabsController):

    events = [
        RefreshEvent,
    ]

    def make(self):
        tabs = list(self.tabs.values())
        number = self.session.get('number', 0)
        try:
            self.context = tabs[number].to_dict()
        except IndexError:
            number = 0
            self.context = tabs[number].to_dict()
        self.session['number'] = number + 1
        self.session.save()

        self.context['timestamp'] = self.timestamp

        self.parse_events()

    def parse_events(self):
        parsers = {}
        for parser in self.events:
            parsers[parser.name] = parser(self.request, self.context)
            parsers[parser.name].prepere()
        timestamp = float(self.GET.get('timestamp', 0))
        for event in self.drivers.slider_event.list_for_command(timestamp):
            parsers[event.name].parse(event)


class RefreshTab(Controller, TabsController):

    def make(self):
        name = self.matchdict['name']
        tab = self.tabs[name]
        self.response = Response(tab())
