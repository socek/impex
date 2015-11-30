from implugin.auth.driver import AuthDriver as BaseAuthDriver

from .models import User


class AuthDriver(BaseAuthDriver):
    model = User
