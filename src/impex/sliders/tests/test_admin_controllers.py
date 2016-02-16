from impex.application.testing import ControllerCase

from ..admin_controllers import SliderAdminController
from ..widgets import SliderAdminFormWidget


class TestSliderAdminController(ControllerCase):
    _object_cls = SliderAdminController

    def test_make(self):
        form = self.madd_form_widget().return_value
        self.madd_flashmsg()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(SliderAdminFormWidget)
        form.validate.assert_called_once_with()
        self.madd_flashmsg().assert_called_once_with('Zapisano.', 'info')

    def test_make_not_validated(self):
        form = self.madd_form_widget().return_value
        form.validate.return_value = None
        self.madd_flashmsg()

        self.object().make()

        self.madd_form_widget().assert_called_once_with(SliderAdminFormWidget)
        form.validate.assert_called_once_with()
        assert self.madd_flashmsg().called is False
