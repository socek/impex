from implugin.auth.driver import AuthDriverHolder

from impex.home.driver import SampleDataDriver
from impex.orders.driver import OrderDriver


class ImpexDriverHolder(AuthDriverHolder):

    @property
    def SampleData(self):
        return self.feeded_driver(SampleDataDriver())

    @property
    def Orders(self):
        return self.feeded_driver(OrderDriver())
