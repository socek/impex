from implugin.sqlalchemy.driver import DriverHolder

from impex.home.driver import SampleDataDriver
from implugin.auth.driver import AuthDriver


class ImpexDriverHolder(DriverHolder):

    def generate_drivers(self):
        super().generate_drivers()
        self.SampleData = self.feeded_driver(SampleDataDriver())
        self.Auth = self.feeded_driver(AuthDriver())
