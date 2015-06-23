from implugin.sqlalchemy.driver import DriverHolder

from impex.home.driver import SampleDataDriver


class ImpexDriverHolder(DriverHolder):

    def generate_drivers(self):
        self.SampleData = self.feeded_driver(SampleDataDriver())
