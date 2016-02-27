from mock import MagicMock
from mock import call

from impex.application.testing import RequestCase
from impex.application.testing import cache

from impex.sliders.tabs import FinalsTabWidget
from impex.sliders.tabs import GroupATabWidget
from impex.sliders.tabs import GroupBTabWidget
from impex.sliders.tabs import LogaTabWidget
from impex.sliders.tabs import ScoresTabWidget
from impex.sliders.tabs import TabList


class TestTabList(RequestCase):

    @cache
    def tab_list(self):
        return TabList(self.mrequest())

    @cache
    def madd_tab(self):
        return self.pobject(TabList, 'add_tab')

    def test_init(self):
        self.madd_tab()

        self.tab_list()

        assert self.madd_tab().call_args_list == [
            call(LogaTabWidget),
            call(ScoresTabWidget),
            call(GroupATabWidget),
            call(GroupBTabWidget),
            call(FinalsTabWidget),
        ]

    def test_add_tab(self):
        tab = MagicMock()
        self.tab_list().tabs = {}

        self.tab_list().add_tab(tab, 'x', y='y')

        tab.assert_called_once_with('x', y='y')
        tab.return_value.feed_request.assert_called_once_with(self.mrequest())

        assert self.tab_list().tabs == {tab.return_value.name: tab.return_value}
