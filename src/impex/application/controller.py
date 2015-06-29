from implugin.fanstatic import FanstaticController

from .requestable import Requestable


class Controller(
    Requestable,
    FanstaticController,
):

    def _generate_resources(self):
        super()._generate_resources()
        self.resources.add_resource('home', 'impex.home.resources:home')
