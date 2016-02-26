from impex.application.requestable import Requestable

from .scores import FinalsTabWidget
from .scores import GroupATabWidget
from .scores import GroupBTabWidget
# from .scores import HighScoresTabWidget
from .scores import ScoresTabWidget
from .slideshow import LogaTabWidget


class TabList(Requestable):

    def __init__(self, request):
        self.feed_request(request)
        self.tabs = []
        self.add_tab(LogaTabWidget)
        self.add_tab(ScoresTabWidget)
        # self.add_tab(HighScoresTabWidget)
        self.add_tab(GroupATabWidget)
        self.add_tab(GroupBTabWidget)
        self.add_tab(FinalsTabWidget)

    def add_tab(self, cls, *args, **kwargs):
        tab = cls(*args, **kwargs)
        tab.feed_request(self.request)
        # self.tabs[tab.name] = tab
        self.tabs.append(tab)
