from implugin.jinja2 import Jinja2Application


class ImpexApplication(Jinja2Application):

    def __init__(self):
        super().__init__('impex')

    def _generate_routes(self):
        self.routing.read_from_file(
            '/home/socek/projects/ex_impex/src/impex/application/routing.yaml'
        )


main = ImpexApplication()
