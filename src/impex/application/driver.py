from implugin.auth.driver import AuthDriverHolder

from impex.home.driver import SampleDataDriver
from impex.orders.driver import OrderDriver


class ImpexDriverHolder(AuthDriverHolder):

    def generate_drivers(self):
        super().generate_drivers()
        self.SampleData = self.feeded_driver(SampleDataDriver())
        self.Orders = self.feeded_driver(OrderDriver())
