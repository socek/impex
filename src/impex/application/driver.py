from implugin.auth.driver import AuthDriverHolder

from impex.orders.driver import OrderDriver
from impex.teams.driver import TeamDriver
from impex.auth.drivers import AuthDriver


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
