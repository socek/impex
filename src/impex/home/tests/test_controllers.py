from implugin.sqlalchemy.testing import SqlalchemyControllerFixture
from implugin.formskit.testing import FormskitControllerFixture

from ..controller import HomeController
from ..forms import FirstForm


class TestHomeController(
    SqlalchemyControllerFixture,
    FormskitControllerFixture,
):

    _testable_cls = HomeController

    def test_simple(
        self,
        testable,
        context,
        mdrivers,
        registry,
        madd_form,
        fform,
        mredirect,
    ):
        fform.validate.return_value = False

        testable.make()

        madd_form.assert_called_once_with(FirstForm)
        assert context == {
            'data': mdrivers.SampleData.find_all.return_value
        }
        assert not mredirect.called

    def test_on_form_submit(
        self,
        testable,
        context,
        mdrivers,
        registry,
        madd_form,
        fform,
        mredirect,
    ):
        fform.validate.return_value = True
        testable.make()

        madd_form.assert_called_once_with(FirstForm)
        assert context == {
            'data': mdrivers.SampleData.find_all.return_value
        }
        mredirect.assert_called_once_with('home')
