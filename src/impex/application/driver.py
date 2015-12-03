from implugin.auth.driver import AuthDriverHolder

from impex.orders.driver import OrderDriver
from impex.teams.driver import TeamDriver
from impex.auth.drivers import AuthDriver
from impex.events.driver import EventDriver
from impex.games.driver import GameDriver


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
