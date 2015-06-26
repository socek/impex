from implugin.beaker import BeakerApplication
from implugin.haml import HamlApplication
from implugin.sqlalchemy.application import SqlAlchemyApplication

from implugin.fanstatic import FanstaticApplication


class ImpexApplication(
    HamlApplication,
    BeakerApplication,
    SqlAlchemyApplication,
    FanstaticApplication,
):

    def __init__(self):
        super().__init__('impex')

    def _generate_routes(self):
        self.routing.read_from_file(self.paths['routing'])


main = ImpexApplication()
