from implugin.fanstatic import FanstaticController
from implugin.formskit.controller import FormskitController
from implugin.flashmsg.controller import FlashMessageController

from .requestable import Requestable


class Controller(
    Requestable,
    FanstaticController,
    FormskitController,
    FlashMessageController,
):

    def _generate_resources(self):
        super()._generate_resources()
        self.resources.add_resource('home', 'impex.home.resources:home')
