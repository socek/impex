from impex.application.controller import Controller

from implugin.auth.controllers import BaseAuthController
from implugin.auth.controllers import ForbiddenController
from implugin.auth.controllers import LoginController
from implugin.auth.controllers import LogoutController
from implugin.auth.controllers import RegisterController

from .forms import ImpexLoginForm


class ImpexBaseAuthController(BaseAuthController, Controller):

    def get_main_template(self):
        return 'impex.application:templates/authencitated.haml'


class ImpexLoginController(LoginController, ImpexBaseAuthController):
    form = ImpexLoginForm
    header_text = 'Impax Login'


class ImpexLogoutController(LogoutController, ImpexBaseAuthController):
    pass


class ImpexForbiddenController(ForbiddenController, ImpexBaseAuthController):
    pass


class ImpexRegisterController(RegisterController, ImpexBaseAuthController):
    pass
