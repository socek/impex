from mock import MagicMock

from impaf.testing import cache
from impaf.testing.case import PyTestCase
from implugin.flashmsg.testing import FlashMessageCase
from implugin.formskit.testing import FormskitControllerCase
from implugin.sqlalchemy.testing import DriverCase as BaseDriverCase
from implugin.sqlalchemy.testing import SqlalchemyCase

from impex.application.init import ImpexApplication


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


class PostFormCase(RequestCase):

    @cache
    def object(self, *args, **kwargs):
        self.mregistry()
        return self._object_cls(self.mrequest())

    @cache
    def mdata(self):
        return self.pobject(self.object(), 'get_data_dict')

    @cache
    def mget_csrf_token(self):
        return self.mrequest().session.get_csrf_token

    @cache
    def mset_value(self):
        return self.pobject(self.object(), 'set_value')

    @cache
    def minstance(self):
        self.object().instance = MagicMock()
        return self.object().instance


class DriverCase(BaseDriverCase):
    _application_cls = ImpexApplication
