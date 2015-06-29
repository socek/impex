from implugin.sqlalchemy.driver import DriverHolder

from impex.home.driver import SampleDataDriver


class ImpexDriverHolder(DriverHolder):

    def generate_drivers(self):
        super().generate_drivers()
        self.SampleData = self.feeded_driver(SampleDataDriver())
