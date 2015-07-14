from implugin.auth.forms import LoginForm
from impex.application.requestable import Requestable


class ImpexLoginForm(LoginForm, Requestable):
    pass
