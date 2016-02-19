from impex.application.requestable import Requestable
from .scores import ScoresTabWidget
from .slideshow import LogaTabWidget
# from .slideshow import SecondTabWidget


class TabList(Requestable):

    def __init__(self, request):
        self.feed_request(request)
        self.tabs = {}
        self.add_tab(LogaTabWidget)
        # self.add_tab(SecondTabWidget)
        self.add_tab(ScoresTabWidget)
        # self.add_tab(ChangeableTabWidget)

    def add_tab(self, cls, *args, **kwargs):
        tab = cls(*args, **kwargs)
        tab.feed_request(self.request)
        self.tabs[tab.name] = tab
