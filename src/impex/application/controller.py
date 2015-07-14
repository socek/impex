from implugin.fanstatic import FanstaticController
from implugin.formskit.controller import FormskitController
from implugin.flashmsg.controller import FlashMessageController

from .requestable import Requestable
from .plugins.flashmessage import ImpexFlashMessageWidget


class Controller(
    Requestable,
    FanstaticController,
    FormskitController,
    FlashMessageController,
):
    _cls_flash_message_widget = ImpexFlashMessageWidget

    def _generate_resources(self):
        super()._generate_resources()
        self.resources.add_resource('home', 'impex.home.resources:home')
        self.resources.add_resource(
            'bootstrap',
            'impex.application.resources:bootstrap',
        )

    def _create_context(self):
        super()._create_context()
        self.context['user'] = self.get_user()
