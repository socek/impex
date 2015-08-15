from impaf.testing.case import PyTestCase
from implugin.flashmsg.testing import FlashMessageCase
from implugin.formskit.testing import FormskitControllerCase
from implugin.sqlalchemy.testing import SqlalchemyCase


class RequestCase(
    SqlalchemyCase,
    PyTestCase,
    FlashMessageCase,
):
    pass


class ControllerCase(
    FormskitControllerCase,
    RequestCase,
):
    pass
