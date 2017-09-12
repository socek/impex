from impaf.testing import ControllerCase
from impaf.testing import PyTestCase

from ..controllers import ImpexBaseAuthController


class TestImpexBaseAuthController(ControllerCase, PyTestCase):
    _object_cls = ImpexBaseAuthController

    def test_get_main_template(self):
        template = self.object().get_main_template()
        return template == 'impex.application:templates/authencitated.haml'
