from implugin.beaker import BeakerApplication
from implugin.haml import HamlApplication
from implugin.sqlalchemy.application import SqlAlchemyApplication


class ImpexApplication(
    HamlApplication,
    BeakerApplication,
    SqlAlchemyApplication,
):

    def __init__(self):
        super().__init__('impex')

    def _generate_routes(self):
        self.routing.read_from_file(
            '/home/socek/projects/impaf/example/src/impex/application/routing.yaml'
        )


main = ImpexApplication()
