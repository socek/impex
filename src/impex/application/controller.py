from implugin.fanstatic import FanstaticController
from implugin.formskit.controller import FormskitController

from .requestable import Requestable


class Controller(
    Requestable,
    FanstaticController,
    FormskitController,
):

    def _generate_resources(self):
        super()._generate_resources()
        self.resources.add_resource('home', 'impex.home.resources:home')
