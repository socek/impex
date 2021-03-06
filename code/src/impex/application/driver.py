from implugin.auth.driver import AuthDriverHolder

from impex.auth.drivers import AuthDriver
from impex.events.driver import EventDriver
from impex.games.driver import GameDriver
from impex.groups.driver import GroupDriver
from impex.orders.driver import OrderDriver
from impex.places.driver import PlaceDriver
from impex.sliders.driver import SliderEventDriver
from impex.sliders.driver import TabDataDriver
from impex.teams.driver import TeamDriver


class ImpexDriverHolder(AuthDriverHolder):

    @property
    def orders(self):
        return self.feeded_driver(OrderDriver())

    @property
    def teams(self):
        return self.feeded_driver(TeamDriver())

    @property
    def auth(self):
        return self.feeded_driver(AuthDriver())

    @property
    def events(self):
        return self.feeded_driver(EventDriver())

    @property
    def games(self):
        return self.feeded_driver(GameDriver())

    @property
    def groups(self):
        return self.feeded_driver(GroupDriver())

    @property
    def places(self):
        return self.feeded_driver(PlaceDriver())

    @property
    def slider_event(self):
        return self.feeded_driver(SliderEventDriver())

    @property
    def tab_data(self):
        return self.feeded_driver(TabDataDriver())
