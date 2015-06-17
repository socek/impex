from implugin.jinja2 import Jinja2Application


class ImpexApplication(Jinja2Application):

    def __init__(self):
        super().__init__('impex')


main = ImpexApplication()
