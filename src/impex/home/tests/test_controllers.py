from implugin.sqlalchemy.testing import SqlalchemyControllerFixture
from implugin.formskit.testing import FormskitControllerFixture

from ..controller import HomeController
from ..forms import FirstForm


class TestHomeController(
    SqlalchemyControllerFixture,
    FormskitControllerFixture,
):

    def _cls_controller(self):
        return HomeController

    def test_simple(
        self,
        controller,
        context,
        mdrivers,
        registry,
        madd_form,
        fform,
        mredirect,
    ):
        fform.validate.return_value = False

        controller.make()

        madd_form.assert_called_once_with(FirstForm)
        assert context == {
            'data': mdrivers.SampleData.find_all.return_value
        }
        assert not mredirect.called

    def test_on_form_submit(
        self,
        controller,
        context,
        mdrivers,
        registry,
        madd_form,
        fform,
        mredirect,
    ):
        fform.validate.return_value = True

        controller.make()

        madd_form.assert_called_once_with(FirstForm)
        assert context == {
            'data': mdrivers.SampleData.find_all.return_value
        }
        mredirect.assert_called_once_with('home')
