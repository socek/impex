from impaf.controller import Controller as Base

from .requestable import Requestable


class Controller(
    Requestable,
    Base,
):
    pass
