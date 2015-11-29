from impaf.testing import cache
from impaf.testing.case import PyTestCase
from implugin.flashmsg.testing import FlashMessageCase
from implugin.formskit.testing import FormskitControllerCase
from implugin.sqlalchemy.testing import SqlalchemyCase


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
