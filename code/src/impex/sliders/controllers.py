from datetime import datetime
from time import mktime

from pyramid.response import Response

from impaf.controller.json import JsonController
from impex.application.controller import Controller
from impex.application.requestable import Requestable
from impex.application.testing import cache

from .events import RefreshEvent
from .tabs import TabList


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

    def make(self):
        self.context['tabs'] = self.tabs.values()
        self.context['timestamp'] = self.timestamp
        self.context['event_id'] = self.event_id


class SliderCommandController(JsonController, Requestable, TabsController):

    events = [
        RefreshEvent,
    ]

    def make(self):
        self._retrive_tabs()
        self._incremenet_tab_number()
        self.context = self._get_tab()
        self.session.save()

        self.context['timestamp'] = self.timestamp

        self.parse_events()

    def _retrive_tabs(self):
        self.tabs_data = list(self.drivers.tab_data.list())

    def _get_tab_number(self):
        return self.session.get('tab_number', 0)

    def _incremenet_tab_number(self):
        tab_number = self._get_tab_number() + 1
        if tab_number >= len(self.tabs_data):
            tab_number = 0
        self.session['tab_number'] = tab_number

    def _get_tab(self):
        data = self.tabs_data[self._get_tab_number()]
        return self.tabs[data.name].to_dict()

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
        try:
            tab = self.tabs[name]
            self.response = Response(tab())
        except:
            pass
