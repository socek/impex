from freezegun import freeze_time
from mock import MagicMock
from mock import sentinel

from impex.application.testing import ControllerCase
from impex.application.testing import cache

from ..controllers import RefreshTab
from ..controllers import SliderCommandController
from ..controllers import SliderShowController
from ..controllers import TabsController


class TestTabsController(ControllerCase):
    _object_cls = TabsController

    @cache
    def object(self, *args, **kwargs):
        self.mregistry()
        obj = self._object_cls()
        obj.request = self.mrequest()
        return obj

    @cache
    def mtab_list(self):
        return self.patch('impex.sliders.controllers.TabList')

    def test_tabs(self):
        self.mtab_list()

        assert self.object().tabs == self.mtab_list().return_value.tabs
        self.mtab_list().assert_called_once_with(self.mrequest())

    @freeze_time("2012-01-14 15:15")
    def test_timestamp(self):
        assert self.object().timestamp == '1326550500'


class TabsControllerCase(ControllerCase):

    @cache
    def mtabs(self):
        tab_list = self.patch('impex.sliders.controllers.TabList')
        return tab_list.return_value


class TestSliderShowController(TabsControllerCase):
    _object_cls = SliderShowController

    @freeze_time("2012-01-14 15:15")
    def test_make(self):
        self.mtabs()
        self.matchdict()['event_id'] = sentinel.event_id

        self.object().make()

        assert self.context() == {
            'tabs': self.mtabs().tabs,
            'timestamp': '1326550500',
            'event_id': sentinel.event_id,
        }


class TestSliderCommandController(TabsControllerCase):
    _object_cls = SliderCommandController

    @cache
    def mincremenet_tab_number(self):
        return self.pobject(self.object(), '_incremenet_tab_number')

    @cache
    def mget_tab(self):
        return self.pobject(self.object(), '_get_tab')

    @cache
    def mparse_events(self):
        return self.pobject(self.object(), 'parse_events')

    def test_incremenet_tab_number(self):
        self.mtabs().tabs = [1, 2, 3]
        session = self.msession()

        self.object()._incremenet_tab_number()
        assert session['tab_number'] == 1

        self.object()._incremenet_tab_number()
        assert session['tab_number'] == 2

        self.object()._incremenet_tab_number()
        assert session['tab_number'] == 0

    def test_get_tab(self):
        one = MagicMock()
        two = MagicMock()
        three = MagicMock()
        self.mtabs().tabs = [one, two, three]
        session = self.msession()
        session['tab_number'] = 1

        assert self.object()._get_tab() == two.to_dict.return_value
        two.to_dict.assert_called_once_with()

    def test_parse_events(self):
        parser = MagicMock()
        event = MagicMock()
        self.object().events = [parser]
        parser.name = 'myname'
        self.context()
        self.mGET()
        self.mdrivers()
        self.mdrivers().slider_event.list_for_command.return_value = [
            event,
        ]
        event.name = 'myname'

        self.object().parse_events()

        parser.assert_called_once_with(self.mrequest(), self.context())
        parser.return_value.prepere.assert_called_once_with()
        self.mdrivers().slider_event.list_for_command.assert_called_once_with(
            0.0
        )
        parser.return_value.parse.assert_called_once_with(event)

    def test_make(self):
        self.mincremenet_tab_number()
        self.mget_tab()
        self.mparse_events()

        self.object().make()

        self.mincremenet_tab_number().assert_called_once_with()
        self.context() == self.mget_tab().return_value
        self.mget_tab().assert_called_once_with()
        self.object().session.save.assert_called_once_with()
        self.mparse_events().assert_called_once_with()


class TestRefreshTab(TabsControllerCase):
    _object_cls = RefreshTab

    @cache
    def mresponse(self):
        return self.patch('impex.sliders.controllers.Response')

    def test_make(self):
        tab = MagicMock()
        self.mtabs().tabs = {'myname': tab}
        self.matchdict()['name'] = 'myname'
        self.mresponse()

        self.object().make()

        assert self.object().response == self.mresponse().return_value
        self.mresponse().assert_called_once_with(tab.return_value)
