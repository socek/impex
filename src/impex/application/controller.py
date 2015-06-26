from impaf.controller import Controller as Base

from .requestable import Requestable
from .resources import static_need


class Controller(
    Requestable,
    Base,
):
    pass

    def _create_context(self):
        super()._create_context()
        self.context['need'] = static_need
