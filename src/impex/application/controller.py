from implugin.fanstatic import FanstaticController
from implugin.flashmsg.controller import FlashMessageController
from implugin.formskit.controller import FormskitController

from .plugins.flashmessage import ImpexFlashMessageWidget
from .requestable import Requestable
from .resources import Resources


class Controller(
    Requestable,
    FanstaticController,
    FormskitController,
    FlashMessageController,
):
    _cls_flash_message_widget = ImpexFlashMessageWidget

    def _generate_resources(self):
        self.resources = Resources()

    def _create_context(self):
        super()._create_context()
        self.context['user'] = self.get_user()
