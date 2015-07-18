from implugin.sqlalchemy.testing import SqlalchemyControllerFixture
from implugin.formskit.testing import FormskitControllerFixture

from ..controller import HomeController
from ..forms import FirstForm


class TestHomeController(
    SqlalchemyControllerFixture,
    FormskitControllerFixture,
):

    _testable_cls = HomeController
