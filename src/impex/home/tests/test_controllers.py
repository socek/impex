from implugin.sqlalchemy.testing import SqlalchemyControllerFixture

from ..controller import HomeController


class TestHomeController(SqlalchemyControllerFixture):

    def _cls_controller(self):
        return HomeController

    def test_simple(self, controller, context, mdrivers):
        controller.make()

        assert context == {
            'data': mdrivers.SampleData.find_all.return_value
        }
