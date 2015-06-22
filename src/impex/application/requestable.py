from implugin.beaker import BeakerRequestable
from implugin.sqlalchemy.requestable import SqlalchemyRequestable

from impex.home.driver import SampleDataDriver


class Requestable(
    SqlalchemyRequestable,
    BeakerRequestable,
):

    def _generate_drivers(self):
        super()._generate_drivers()
        self.SampleData = self.feeded_driver(SampleDataDriver())
