from implugin.auth.driver import AuthDriverHolder

from impex.home.driver import SampleDataDriver


class ImpexDriverHolder(AuthDriverHolder):

    def generate_drivers(self):
        super().generate_drivers()
        self.SampleData = self.feeded_driver(SampleDataDriver())
