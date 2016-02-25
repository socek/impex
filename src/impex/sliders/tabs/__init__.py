from impex.application.requestable import Requestable
from .scores import ScoresTabWidget
from .slideshow import LogaTabWidget


class TabList(Requestable):

    def __init__(self, request):
        self.feed_request(request)
        self.tabs = {}
        self.add_tab(LogaTabWidget)
        self.add_tab(ScoresTabWidget)

    def add_tab(self, cls, *args, **kwargs):
        tab = cls(*args, **kwargs)
        tab.feed_request(self.request)
        self.tabs[tab.name] = tab
